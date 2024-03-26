import json
import pickle

import numpy as np
import numpy.typing as npt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor  # type: ignore[import-untyped]

from src.data.get_flight_stats import FlightStats
from src.data.get_runway_stats import RunwayStats
from src.types.airport import Airport
from src.utils.json_converter import DataConverter


class Model:

    def __init__(self) -> None:
        self._model = None  # type: RandomForestRegressor

    @classmethod
    def load_trained_model(cls, filename: str) -> 'Model':
        with open(filename, 'rb') as f:
            model = pickle.load(f)
        instance = cls()
        if not isinstance(model, RandomForestRegressor):
            raise AttributeError(
                f'The file {filename!r} does not contain a valid model. '
                f'Expected type {type(RandomForestRegressor)!r} but got {type(model)!r} '
            )
        instance._model = model
        return instance

    def predict(self, prepped_input: pd.DataFrame) -> npt.NDArray[np.float32]:
        return self._model.predict(prepped_input)

    def train(self, data_filename: str) -> 'Model':
        with open(data_filename, 'r', encoding='utf-8') as f:
            print(next(f))
            raw_data = json.load(f)
        target, features = self.preprocessing(raw_data)
        return self.fit(features, target)

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> 'Model':
        self._model = RandomForestRegressor(criterion='friedman_mse', max_depth=80, max_features=1,
                      min_samples_leaf=4, min_samples_split=10,
                      n_estimators=50)
        self._model.fit(features, target.values.ravel())
        return self

    def save_trained_model(self, filename: str) -> None:
        with open(filename, 'wb') as f:
            pickle.dump(self._model, f)

    def preprocessing(self, raw_data: dict[str, list[Airport]]) -> tuple[pd.DataFrame, pd.DataFrame]:
        # convert feature data
        airport_data = DataConverter(raw_data)
        airport_df = airport_data.airports_df
        flights_df = airport_data.flights
        flights_df = pd.concat([flights_df, airport_df['iata']], axis=1, join='outer')
        runways_df = airport_data.runways
        runways_df = pd.concat([runways_df, airport_df['iata']], axis=1, join='outer')

        # get runway and flight stats for feature data
        runways_stats = RunwayStats(runways_df)
        flights_stats = FlightStats(flights_df)
        runway_stats_df = runways_stats.runways_stats_df
        flights_stats_df = flights_stats.flight_stats_df

        # drop useless features, concat engineered features
        airport_df = airport_df.drop(['country', 'icao', 'name'], axis=1)
        full_airports_df = pd.merge(airport_df, runway_stats_df, on = 'iata')
        full_airports_df = pd.merge(full_airports_df, flights_stats_df, on = 'iata')
        # drop all rows with duplicate iata data
        full_airports_df = full_airports_df.drop_duplicates(subset=['iata'])

        # drop all rows with null data
        full_airports_df = full_airports_df.dropna()
        full_airports_df = full_airports_df.loc[full_airports_df['runways_count'] != 0]

        # set iata as the index
        full_airports_df.set_index('iata', inplace=True)

        # separate features and target data
        target = full_airports_df[['air_quality']]
        features = full_airports_df.drop(['air_quality'], axis=1)
        features['altitude'] = features['altitude'].astype(float)
        return target, features
