import json
import unittest

import pandas as pd
import pandas.testing as pd_testing

from src.data.get_runway_stats import RunwayStats
from src.utils.json_converter import DataConverter


class TestRunwayStats(unittest.TestCase):
    RUNWAYS_STATS = [
        'iata',
        'runways_count',
        'total_runway_length'
        ]

    def assertDataframeEqual(self, a: pd.DataFrame, b: pd.DataFrame, msg: None = None) -> None:
        try:
            pd_testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self) -> None:
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_runway_stats_structure(self) -> None:
        data_path = 'data/tests/model_test_subset_dataset.json'
        with open(data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        airport_data = DataConverter(raw_data)
        runways_df = pd.concat([airport_data.runways, airport_data.airports_df['iata']], axis=1, join='outer')
        runway_stats = RunwayStats(runways_df)
        runways_stats_df = runway_stats.runways_stats_df

        self.assertTrue(all(isinstance(count, int) for count in runways_stats_df['runways_count']))
        self.assertTrue(all(isinstance(count, int) for count in runways_stats_df['total_runway_length']))
        self.assertIsInstance(runways_stats_df, pd.DataFrame)
        self.assertEqual(set(runways_stats_df.columns), set(self.RUNWAYS_STATS))
        self.assertEqual(runways_stats_df.shape[1], len(self.RUNWAYS_STATS))

    def test_count_runways_logic_basecase(self) -> None:
        # base test case
        empty_runways_stats_input_df = pd.DataFrame(
            [
                {
                    'iata': 'YVR',
                    'runways': []
                }
            ]
        )
        empty_runways_stats = RunwayStats(empty_runways_stats_input_df)
        fake_output_empty = pd.DataFrame(
            {
            'iata': ['YVR'],
            'runways_count': [0],
            'total_runway_length': [0],
            }
        )
        self.assertEqual(empty_runways_stats.runways_stats_df, fake_output_empty)

    def test_count_runways_logic_empty_runways(self) -> None:
        # test output is 0 if the runways lists are empty
        runways_input_df = pd.DataFrame(
            [
                {
                    'iata': 'YVR',
                    'runways': [
                        {'length_in_ft': 20},
                        {'length_in_ft': 50}
                    ]
                }
            ]
        )
        runways_stats = RunwayStats(runways_input_df)
        fake_output_empty = pd.DataFrame(
            {
            'iata': ['YVR'],
            'runways_count': [2],
            'total_runway_length': [70]
            }
        )
        self.assertEqual(runways_stats.runways_stats_df, fake_output_empty)

    def test_sum_runways_len_throws_exception(self) -> None:
        # how does negative lengths affect
        fake_input_runways_df = pd.DataFrame(
            {
                'iata': 'YVR',
                'runways': [
                    [
                        {'length_in_ft': 20},
                        {'length_in_ft': -20}
                    ]
                ]
            }
        )
        with self.assertRaises(ValueError):
            RunwayStats(fake_input_runways_df)

if __name__ == '__main__':
    unittest.main()
