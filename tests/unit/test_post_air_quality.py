import os
import unittest
from unittest import TestResult

from fastapi.testclient import TestClient

from src.api.errors import ForbiddenError, UnauthorizedError
from src.main import app


class TestPostAirQuality(unittest.TestCase):
    api_key: str = ''
    data = {
        'altitude': 10000,
        'runways': [
            {
                'surface': 'concrete',
                'length_in_ft': 5000
            }
        ],
        'total_arrivals': 100,
        'total_departures': 50
    }

    @classmethod
    def setUpClass(cls) -> None:
        api_key = 'GaezpTQ5QY9P18CfRj8Fwg=='
        os.environ['API_KEY'] = api_key
        cls.api_key = api_key

    @classmethod
    def tearDownClass(cls) -> None:
        os.unsetenv('__API_KEY')

    def run(self, result: TestResult | None = None) -> None:
        with TestClient(app) as client:
            self.test_client = client
            super().run(result)

    def test_post_air_quality_success(self) -> None:
        resp = self.test_client.post('/air-quality', json=self.data, headers={'X-API-KEY': self.api_key})
        # Response code should be 201
        self.assertEqual(resp.status_code, 201)
        resp_json = resp.json()
        # There should only be one key in the response
        self.assertCountEqual(['air_quality'], resp_json.keys())
        print(resp_json['air_quality'])
        self.assertTrue(20 <= resp_json['air_quality'] <= 40)

    def test_predict_with_multiple_runways(self) -> None:
        airport_data = {
            'altitude': 10000,
            'runways': [
                {
                    'surface': 'concrete',
                    'length_in_ft': 9855
                },
                {
                    'surface': 'asphalt',
                    'length_in_ft': 7623
                }
            ],
            'total_arrivals': 100,
            'total_departures': 50
        }
        resp = self.test_client.post('/air-quality', json=airport_data, headers={'X-API-KEY': self.api_key})
        self.assertEqual(resp.status_code, 201)
        resp_json = resp.json()
        # There should only be one key in the response
        self.assertCountEqual(['air_quality'], resp_json)
        # Check the air quality is approximately correct
        print(resp_json['air_quality'])
        self.assertTrue(20 <= resp_json['air_quality'] <= 40)

    def test_can_predict_with_no_runways(self) -> None:
        airport_data = {
            'altitude': 10000,
            'total_arrivals': 100,
            'runways': [],
            'total_departures': 50
        }
        resp = self.test_client.post('/air-quality', json=airport_data, headers={'X-API-KEY': self.api_key})
        self.assertEqual(resp.status_code, 201)
        self.assertCountEqual(['air_quality'], resp.json())
        print(resp.json()['air_quality'])
        self.assertTrue(30 <= resp.json()['air_quality'] <= 50)

    def test_predict_fails_with_bad_api_key(self) -> None:
        api_key = 'some_bad_api_key'
        resp = self.test_client.post('/air-quality', json=self.data, headers={'X-API-KEY': api_key})
        self.assertEqual(resp.status_code, 401)
        resp_json = resp.json()
        # There should be exactly two key in the error response
        self.assertCountEqual(['errors', 'status_code'], resp_json)
        # The status code should match that of the response
        self.assertEqual(resp_json['status_code'], resp.status_code)
        # There should be exactly one error
        self.assertEqual(len(resp_json['errors']), 1)
        # The error should be an `UnauthorizedError`
        self.assertEqual(resp_json['errors'][0], UnauthorizedError().json())

    @unittest.skip('Response model for missing API key is inconsistent with API schema')
    def test_predict_fails_with_missing_api_key(self) -> None:
        resp = self.test_client.post('/air-quality', json=self.data)
        self.assertEqual(resp.status_code, 403)
        # FIXME: This doesn't return the correct error response
        resp_json = resp.json()
        # There should be exactly two key in the error response
        self.assertCountEqual(['errors', 'status_code'], resp_json)
        # The status code should match that of the response
        self.assertEqual(resp_json['status_code'], resp.status_code)
        # There should be exactly one error
        self.assertEqual(len(resp_json['errors']), 1)
        # The error should be an `UnauthorizedError`
        self.assertEqual(resp_json['errors'][0], ForbiddenError().json())

    def test_all_fields_are_required(self) -> None:
        test_data = self.data.copy()
        # Altitude should be a required field
        del test_data['altitude']
        resp = self.test_client.post('/air-quality', json=test_data, headers={'X-API-KEY': self.api_key})
        # Should get a 422 when altitude is missing
        self.assertEqual(resp.status_code, 422)

        # Check total_arrivals is a required field
        test_data = self.data.copy()
        del test_data['total_arrivals']
        resp = self.test_client.post('/air-quality', json=test_data, headers={'X-API-KEY': self.api_key})
        self.assertEqual(resp.status_code, 422)

        # Check total_departures is a required field
        test_data = self.data.copy()
        del test_data['total_departures']
        resp = self.test_client.post('/air-quality', json=test_data, headers={'X-API-KEY': self.api_key})
        self.assertEqual(resp.status_code, 422)

        # Check runways is a required field
        test_data = self.data.copy()
        del test_data['runways']
        resp = self.test_client.post('/air-quality', json=test_data, headers={'X-API-KEY': self.api_key})
        self.assertEqual(resp.status_code, 422)


if __name__ == '__main__':
    unittest.main()
