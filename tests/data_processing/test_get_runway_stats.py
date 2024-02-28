import json
import unittest

import pandas as pd

from src.data.get_runway_stats import RunwayStats
from src.utils.json_converter import DataConverter


class TestFlightStats(unittest.TestCase):
    RUNWAYS_STATS = [
        'runways',
        'total_runway_length'
        ]

    def setUp(self) -> None:
        self.data_path = 'data/tests/model_test_subset_dataset.json'
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        self.airport_data = DataConverter(self.raw_data)
        runways_df = self.airport_data.runways
        self.runway_stats = RunwayStats(runways_df)

        #create empty runways dataframe
        empty_data: pd.DataFrame = {'runways': [[],[]]}
        runways_df_empty = pd.DataFrame(empty_data)
        self.empty_runway_stats = RunwayStats(runways_df_empty)

    def test_runway_stats_output(self) -> None:
        # check output is a dataframe
        self.assertIsInstance(self.runway_stats.runways_stats_df, pd.DataFrame)
        # test column names of runway stats output
        self.assertEqual(set(self.runway_stats.runways_stats_df.columns), set(self.RUNWAYS_STATS))
        # test shape of runway stats output
        self.assertEqual(self.runway_stats.runways_stats_df.shape[1], len(self.RUNWAYS_STATS))

    def test_count_runways(self) -> None:
        runway_stats_int = self.runway_stats.runways_stats_df.dropna()
        self.assertTrue(all(isinstance(y, float) for y in runway_stats_int['runways']))

        self.assertTrue(all(y is None for y in self.empty_runway_stats.runways_stats_df['runways']))

    ## test count runways
        # test type output is int or None
        # check that empty input returns None

    def test_sum_runways_len(self) -> None:

        runway_stats_int = self.runway_stats.runways_stats_df.dropna()
        self.assertTrue(all(isinstance(y, float) for y in runway_stats_int['total_runway_length']))

        self.assertTrue(all(y is None for y in self.empty_runway_stats.runways_stats_df['total_runway_length']))
    ## test sum_runways_len
        # test type output is int or None
        # check that empty input returns None
        # Bad user input: test error message when runwayDict columns are wrong
        # Bad user input: test error message if length_in_ft is a str or something else
        # Bad user input: test what happens if length in ft is entered as a negative number


if __name__ == '__main__':
    unittest.main()
