import pickle
import json

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.data.get_runway_stats import RunwayStats
from src.data.get_flight_stats import FlightStats
from src.utils.json_converter import DataConverter
from src.types.airport import Airport


class Model:
    def __init__(self) -> None:
        self._model = None  # type: RandomForestRegressor

    def load_trained_model(self, filename: str) -> None:
        with open(filename, "rb") as f:
            model = pickle.load(f)
        if not isinstance(model, RandomForestRegressor):
            raise AttributeError(
                f"The file {filename!r} does not contain a valid model. "
                f"Expected type {type(RandomForestRegressor)!r} but got {type(model)!r} "
            )
        self._model = model

    def predict(self, prepped_input: pd.DataFrame) -> float:
        return self._model.predict(prepped_input)

    def train(self, data_filename: str) -> "Model":
        with open(data_filename, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        target, features = self.preprocessing(raw_data)
        return self.fit(features, target)

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> "Model":
        self._model = RandomForestRegressor(n_estimators=10, max_features=2)
        self._model.fit(features, target.values.ravel())
        return self

    def save_trained_model(self, filename: str) -> None:
        with open(filename, "wb") as f:
            pickle.dump(self._model, f)

    def preprocessing(self, raw_data: dict[str, list[Airport]]) -> tuple[pd.DataFrame, pd.DataFrame]:
        # convert feature data
        airport_data = DataConverter(raw_data)
        airport_df = airport_data.airports_df
        flights_json = airport_data.flights
        runways_json = airport_data.runways

        # get runway and flight stats for feature data
        runways_stats = RunwayStats(runways_json)
        flights_stats = FlightStats(flights_json)
        runway_df = runways_stats.runways_stats_df
        flights_df = flights_stats.flight_stats_df

        # drop useless features, concat engineered features
        airport_df = airport_df.drop(["country", "icao", "name"], axis=1)
        full_airports_df = pd.concat([airport_df, runway_df, flights_df], axis=1)

        # combine the dataframes, set iata as the index
        full_airports_df.set_index("iata", inplace=True)

        # drop all rows with null data
        full_airports_df = full_airports_df.dropna()

        # separate features and target data
        target = full_airports_df[["air_quality"]]
        features = full_airports_df.drop(["air_quality"], axis=1)
        return target, features
