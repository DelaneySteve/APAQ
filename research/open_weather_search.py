"""
Testing the IQAir API to use a list of airport locations
to search and find air quality measurements within a particular
distance from those locations.

IMPORTANT:
- This file must be run BEFORE the "combine_aq_airports_data.py" file
- This file requires a configuration file to run successfully
- The configuration file must be in the "research" directory and be named "config.yaml"
- The configuration file must at least contain the following:

api_keys:
    open_weather: str (API key to access OpenWeather)

"""

import csv
import logging
import pandas as pd
import requests
import yaml
from yaml.loader import SafeLoader

# obtain API key from config file
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=SafeLoader)

OPEN_WEATHER_API_KEY = config["api_keys"]["open_weather"]
AIR_QUALITY_DUMP_PATH = config["file_paths"]["air_quality"]
AIRPORTS_FILE_PATH = "../data/iata-icao.csv"
ICAO_INDEX = 3
IATA_INDEX = 2
LAT_INDEX = 5
LON_INDEX = 6

airports_iata = []
airports_icao = []
airports_lat = []
airports_lon = []
airports_pm10 = []


# Open the file with specified encoding
with open(AIRPORTS_FILE_PATH, "r", encoding="utf-8") as file:
    next(file) # skips header
    csv_reader = csv.reader(file)
    data = []
    for line in csv_reader:
        # Process each line here
        processed_line = [cell.encode("unicode_escape").decode("utf-8") for cell in line]
        curr_icao = processed_line[ICAO_INDEX]
        curr_iata = processed_line[IATA_INDEX]
        curr_lat = processed_line[LAT_INDEX]
        curr_lon = processed_line[LON_INDEX]

        url = "http://api.openweathermap.org/data/2.5/air_pollution?lat=" + curr_lat + "&lon=" + curr_lon + "&appid=" + OPEN_WEATHER_API_KEY

        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            result = response.json()
            # Process "result" as needed
            try:
                airports_pm10.append(float(result["list"][0]["components"]["pm10"]))
                airports_icao.append(curr_icao)
                airports_iata.append(curr_iata)
                airports_lat.append(curr_lat)
                airports_lon.append(curr_lon)

            except KeyError:
                curr_pm10 = None
        else:
            logging.info("Request failed with status code %s", str(response.status_code))

airports_df = pd.DataFrame({
                            "iata": airports_iata,
                            "icao": airports_icao,
                            "latitude": airports_lat,
                            "longitude": airports_lon,
                            "pm10": airports_pm10
                            })

airports_df.to_csv(AIR_QUALITY_DUMP_PATH, sep="\t")
