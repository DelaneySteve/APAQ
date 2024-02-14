import json
import unittest

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score  # type: ignore [import-untyped]
from sklearn.model_selection import train_test_split  # type: ignore [import-untyped]

from src.model.model import Model


class TestModel(unittest.TestCase):
    FEATURE_COLUMNS = [
        'altitude',
        'runways',
        'total_runway_length',
        'total_arrivals',
        'total_departures',
    ]
    TARGET = ['air_quality']

    def setUp(self) -> None:
        self.model = Model()
        self.data_path = 'data/unit_tests/model/mock_airport_dataset.json'
        self.model_path = 'src/model/model_new.pickle'
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)

    def test_loading_wrong_model(self) -> None:
        wrong_model_path = 'data/unit_tests/model/lr_model.pickle'

        # check attribute error is raised when loading the wrong model type
        test_model_class = Model()
        with self.assertRaises(AttributeError):
            test_model_class.load_trained_model(wrong_model_path)

    def test_data_preprocessing(self) -> None:
        targets, features = self.model.preprocessing(self.raw_data)
        self.assertIsInstance(features, pd.DataFrame)
        self.assertIsInstance(targets, pd.DataFrame)
        self.assertEqual(features.shape[1], len(self.FEATURE_COLUMNS))
        self.assertEqual(targets.shape[1], len(self.TARGET))
        self.assertEqual(set(features.columns), set(self.FEATURE_COLUMNS))
        self.assertEqual(set(targets.columns), set(self.TARGET))

    def test_fit(self) -> None:
        targets, features = self.model.preprocessing(self.raw_data)
        x_train, x_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=0)
        self.model.fit(x_train, y_train)
        y_pred = self.model.predict(x_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        self.assertGreaterEqual(r2, 0.01)
        self.assertLessEqual(rmse, 50)
        self.assertLessEqual(mae, 30)

    def test_predict(self) -> None:
        targets, features = self.model.preprocessing(self.raw_data)
        x_train, x_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=0) #pylint: disable = unused-variable, line-too-long
        self.model.fit(x_train, y_train)
        y_pred = self.model.predict(x_test)
        self.assertTrue(all(isinstance(y, float) for y in y_pred))

if __name__ == '__main__':
    unittest.main()
