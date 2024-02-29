import json
import unittest

import pandas as pd

from src.data.get_runway_stats import RunwayStats
from src.utils.json_converter import DataConverter


class TestRunwayStats(unittest.TestCase):
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
        runways_df = runways_df[runways_df['runways'].apply(len) > 0]
        runway_stats = RunwayStats(runways_df)
        self.runways_stats_df = runway_stats.runways_stats_df

    def test_runway_stats_output(self) -> None:
        self.assertIsInstance(self.runways_stats_df, pd.DataFrame)
        self.assertEqual(set(self.runways_stats_df.columns), set(self.RUNWAYS_STATS))
        self.assertEqual(self.runways_stats_df.shape[1], len(self.RUNWAYS_STATS))

    def test_count_runways(self) -> None:
        self.assertTrue(all(isinstance(count, int) for count in self.runways_stats_df['runways']))

    def test_sum_runways_len(self) -> None:
        self.assertTrue(all(isinstance(length, int) for length in self.runways_stats_df['total_runway_length']))

    def test_sum_runways_len_throws_exception(self) -> None:
        fake_input_data = {'runways': [[{'length_in_ft': 20},{'length_in_ft': -20}]]}
        fake_input_runways_df = pd.DataFrame(fake_input_data)
        with self.assertRaises(ValueError):
            RunwayStats(fake_input_runways_df)

if __name__ == '__main__':
    unittest.main()
