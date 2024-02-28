import json
import unittest

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

    ## GENERAL: Test regular data input of runway stats
        # test shape of runway stats output
        # test column names of runway stats output
        # check output is a dataframe

    ## test count runways
        # test type output is int or None
        # check that empty input returns None

    ## test sum_runways_len
        # test type output is int or None
        # check that empty input returns None
        # Bad user input: test error message when runwayDict columns are wrong
        # Bad user input: test error message if length_in_ft is a str or something else
        # Bad user input: test what happens if length in ft is entered as a negative number
