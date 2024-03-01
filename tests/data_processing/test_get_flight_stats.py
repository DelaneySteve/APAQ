import json
import unittest

import pandas as pd
import pandas.testing as pd_testing

from src.data.get_flight_stats import FlightStats
from src.utils.json_converter import DataConverter


class TestFlightStats(unittest.TestCase):
    FLIGHT_COUNT = [
        'total_arrivals',
        'total_departures'
    ]

    def assertDataframeEqual(self, a: pd.DataFrame, b: pd.DataFrame, msg: None = None) -> None:
        try:
            pd_testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self) -> None:
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_count_flights_empty(self) -> None:
        # check output is 0 if the flight lists are empty
        empty_flights_stats = FlightStats(pd.DataFrame({'flights': [[], [], [], []]}))
        self.assertTrue(all(count == 0 for count in empty_flights_stats.flight_stats_df['total_arrivals']))
        self.assertTrue(all(count == 0 for count in empty_flights_stats.flight_stats_df['total_departures']))

    def test_count_flights(self) -> None:
        self.data_path = 'data/tests/model_test_subset_dataset.json'
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        self.airport_data = DataConverter(self.raw_data)

        flights_stats = FlightStats(self.airport_data.flights)
        # check output dataframe types are int
        self.assertTrue(all(isinstance(count, int) for count in flights_stats.flight_stats_df['total_arrivals']))
        self.assertTrue(all(isinstance(count, int) for count in flights_stats.flight_stats_df['total_departures']))
        # check output shape
        self.assertEqual(flights_stats.flight_stats_df.shape[1], len(self.FLIGHT_COUNT))
        # check column names are as expected
        self.assertEqual(set(flights_stats.flight_stats_df.columns), set(self.FLIGHT_COUNT))
        # check output is a dataframe
        self.assertIsInstance(flights_stats.flight_stats_df, pd.DataFrame)

    def test_count_flights_logic(self) -> None:
        # base test case
        fake_input_flights_df = pd.DataFrame(
            {
                'flights': [
                    [
                        {'origin_iata': 'LBG'},
                        {'origin_iata': 'LBG'},
                        {'origin_iata': 'LBG'},
                        {'origin_iata': 'SAY'},
                        {'origin_iata': 'YVR'}
                    ]
                ]
            }
        )
        flights_stats = FlightStats(fake_input_flights_df)

        fake_output_flights_df = pd.DataFrame(
            {
            'total_arrivals': [2],
            'total_departures': [3]
            }
        )
        self.assertEqual(flights_stats.flight_stats_df, fake_output_flights_df)

        # test output is 0 if the flight lists are empty
        empty_flights_stats_df = pd.DataFrame(
            {
                'flights':
                [
                    [],
                    [],
                    [],
                    []
                ]
            }
        )
        empty_flights_stats = FlightStats(empty_flights_stats_df)
        self.assertTrue(all(count == 0 for count in empty_flights_stats.flight_stats_df['total_arrivals']))
        self.assertTrue(all(count == 0 for count in empty_flights_stats.flight_stats_df['total_departures']))

        # test output is 0 for arrivals if there are no arrivals
        fake_input_flights_no_arr = pd.DataFrame(
            {
                'flights': [
                    [
                        {'origin_iata': 'LBG'},
                        {'origin_iata': 'LBG'},
                        {'origin_iata': 'LBG'},
                    ]
                ]
            }
        )

        flights_stats = FlightStats(fake_input_flights_no_arr)

        fake_output_np_arr_df = pd.DataFrame(
            {
            'total_arrivals': [0],
            'total_departures': [3]
            }
        )
        self.assertEqual(flights_stats.flight_stats_df, fake_output_np_arr_df)

        # Doesn't work yet, needs to be fixed in model and get_flight_stats

        ## test output is 0 for departures if there are no arrivals
        #fake_input_flights_no_dep = pd.DataFrame(
        #    {
        #        'flights': [
        #            [
        #                {'origin_iata': 'SAY'},
        #                {'origin_iata': 'YVR'}
        #            ]
        #        ]
        #    }
        #)

        #flights_stats = FlightStats(fake_input_flights_no_dep)

        #fake_output_np_dep_df = pd.DataFrame(
        #    {
        #    'total_arrivals': [2],
        #    'total_departures': [0]
        #    }
        #)
        #self.assertEqual(flights_stats.flight_stats_df, fake_output_np_dep_df)



if __name__ == '__main__':
    unittest.main()
