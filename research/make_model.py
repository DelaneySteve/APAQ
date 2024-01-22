"""
    Allows for the preprocessing a dataset
    of airport data; and using it to then make, 
    train, and save a Random Forest Regression model. 
"""

import pickle
import json
from sklearn.ensemble import RandomForestRegressor #type: ignore [import-untyped]
import pandas as pd
from data.json_converter import DataConverter
from data.stats.get_runway_stats import RunwayStats
from data.stats.get_flight_stats import FlightStats
from src.data.types import Airport

class MakeModel:
    def __init__(self) -> None:
        self._model = RandomForestRegressor(n_estimators=10, max_features=2)

    def train_fit(self, data_filename: str, save_filename: str) -> "MakeModel":
        with open(data_filename, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        target, features = self.preprocessing(raw_data)
        self._model.fit(features,target.values.ravel())
        self.__save_trained_model(save_filename)
        return self

    def __save_trained_model(self, filename: str) -> None:
        with open(filename, 'wb') as f:
            pickle.dump(self._model,f)

    def preprocessing(self,
                      raw_data: dict[str, list[Airport]]) -> tuple[pd.DataFrame, pd.DataFrame]:
        # convert feature data
        airport_data = DataConverter(raw_data)
        airport_df = airport_data.airports_df
        flights_json = airport_data.flights
        runways_json = airport_data.runways

        # get runway and flight stats for feature data
        runways_stats = RunwayStats(runways_json)
        flights_stats = FlightStats(flights_json)
        runway_df = runways_stats.runway_df()
        flights_df = flights_stats.flight_count_df()


        # drop useless features, concat engineered features
        airport_df = airport_df.drop(['country','icao','name'],axis = 1)
        full_airports_df = pd.concat([airport_df,runway_df,flights_df], axis= 1)

        # combine the dataframes, set iata as the index
        full_airports_df.set_index('iata',inplace = True)

        # drop all rows with null data
        full_airports_df = full_airports_df.dropna()

        # separate features and target data
        target = full_airports_df[['air_quality']]
        features = full_airports_df.drop(["air_quality"],axis=1)
        return target, features
