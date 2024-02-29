import json
import unittest
from typing import Any

import pandas as pd

from src.data.get_flight_stats import FlightStats
from src.utils.json_converter import DataConverter


class TestFlightStats(unittest.TestCase):
    FLIGHT_COUNT = [
        'total_arrivals',
        'total_departures'
        ]

    def setUp(self) -> None:
        self.data_path = 'data/tests/model_test_subset_dataset.json'
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        self.airport_data = DataConverter(self.raw_data)

    def test_count_flights_empty(self) -> None:
        # check output is 0 if the flight lists are empty
        empty_data = {'flights': [[], [], [], []]} #type: dict[str, list[Any]]
        flights_df_empty = pd.DataFrame(empty_data)
        empty_flights_stats = FlightStats(flights_df_empty)
        self.assertTrue(all(y == 0 for y in empty_flights_stats.flight_stats_df['total_arrivals']))
        self.assertTrue(all(y == 0 for y in empty_flights_stats.flight_stats_df['total_departures']))

    def test_count_flights(self) -> None:
        flights_df = self.airport_data.flights
        flights_stats = FlightStats(flights_df)
        # check output dataframe types are int
        self.assertTrue(all(isinstance(y, int) for y in flights_stats.flight_stats_df['total_arrivals']))
        self.assertTrue(all(isinstance(y, int) for y in flights_stats.flight_stats_df['total_departures']))
        # check output shape
        self.assertEqual(flights_stats.flight_stats_df.shape[1], len(self.FLIGHT_COUNT))
        # check column names are as expected
        self.assertEqual(set(flights_stats.flight_stats_df.columns), set(self.FLIGHT_COUNT))
        # check output is a dataframe
        self.assertIsInstance(flights_stats.flight_stats_df, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
