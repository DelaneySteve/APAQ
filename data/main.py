import json
import pandas as pd
from  data.stats import get_runway_stats
from data.stats import get_flight_stats
from data import json_converter




FILENAME = "C:/Users/delan/Documents/APAQ_files/Airports.json"
with open(FILENAME, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

airportData = json_converter.DataConverter(raw_data)
airport_df = airportData.airports_df
flights_json = airportData.flights
runways_json = airportData.runways

runways_stats = get_runway_stats.RunwayStats(runways_json)
flights_stats = get_flight_stats.FlightStats(flights_json)
runway_df = runways_stats.runway_df()
flights_df = flights_stats.flight_count_df()

full_airports_df = pd.concat([airport_df,runway_df,flights_df], axis= 1)

SAVE_FILE = "C:/Users/delan/Documents/APAQ_files/final_airport_df.csv"
full_airports_df.to_csv(SAVE_FILE, sep=",", index=False, encoding="utf-8")
