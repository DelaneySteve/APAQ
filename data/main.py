import json
from data import json_converter
import pandas as pd
from  data.stats import runway_stats
from data.stats import flight_stats


filename = "C:/Users/delan/Downloads/Airports.json"
with open(filename, "r", encoding="utf-8") as f:
        raw_data = json.load(f)    
airportData = json_converter.DataConverter(raw_data)

airport_df = airportData.airports_df
flights_json = airportData.flights
runways_json = airportData.runways

runways_stats = runway_stats.RunwayStats(runways_json)
flights_stats = flight_stats.FlightStats(flights_json)
runway_df = runways_stats.runway_df()
flights_df = flights_stats.flight_count_df()

full_airports_df = pd.concat([airport_df,runway_df,flights_df], axis= 1)
print(full_airports_df.dropna().info())