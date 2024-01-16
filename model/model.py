from itertools import repeat
import pandas as pd
import numpy as np
from data import json_converter
from  data.stats import get_runway_stats
from data.stats import get_flight_stats


class Model:

    def preprocessing(self, raw_data: pd.DataFrame,
                      target: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        # convert feature data
        airport_data = json_converter.DataConverter(raw_data)
        airport_df = airport_data.airports_df
        flights_json = airport_data.flights
        runways_json = airport_data.runways

        # get runway and flight stats for feature data
        runways_stats = get_runway_stats.RunwayStats(runways_json)
        flights_stats = get_flight_stats.FlightStats(flights_json)
        runway_df = runways_stats.runway_df()
        flights_df = flights_stats.flight_count_df()


        # drop useless features, concat engineered features
        airport_df = airport_df.drop(['country','icao','name'],axis = 1)
        full_airports_df = pd.concat([airport_df,runway_df,flights_df], axis= 1)

        ### edit air quality json and match it to the feature dataset
        raw_aq_df = pd.DataFrame(target["airports"])
        raw_aq_df = raw_aq_df[['iata','air quality']]
        raw_aq_df['air quality'] = raw_aq_df['air quality'].astype(float)

        aq_df = pd.DataFrame(list(map(link_aq_to_data, full_airports_df['iata'],
                                      repeat(raw_aq_df))), columns = ["air_quality"])

        # combine the dataframes, set iata as the index 
        full_airports_df = pd.concat([full_airports_df,aq_df], axis = 1)
        full_airports_df.set_index('iata',inplace = True)

        # drop all rows with null data
        full_airports_df = full_airports_df.dropna()

        # separate features and target data
        features = full_airports_df.drop(["air_quality"],axis=1)
        target = full_airports_df[['air_quality']].copy()

        return target, features

def link_aq_to_data(data_airport, raw_aq_df):
    x = np.where(raw_aq_df['iata'] == data_airport, raw_aq_df["air quality"],None)
    aq_data = list(filter(lambda item: item is not None,x ))
    if not aq_data:
        aq_data = None
    else:
        aq_data = aq_data[0]
    return aq_data

