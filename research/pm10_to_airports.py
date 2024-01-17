""" Testing the IQAir API to use a list of airport locations
to search and find air quality measurements within a particular
distance from those locations.
"""

import argparse
from argparse import ArgumentParser
import csv
import json
import logging
import pandas as pd
import requests
import yaml
from yaml.loader import SafeLoader

# allow logger to display INFO level logs
logging.basicConfig(level = logging.INFO)

parser = ArgumentParser(description="Read file form Command line.")
parser.add_argument("--ow-api-key", dest="open_weather_api_key", required=True, type=str, help="open weather API key")
parser.add_argument("--airports-load-file", dest="airports_load_file", required=True, type=str, help="general information of each airport file path")
parser.add_argument("--airports-dump-dir", dest="airports_dump_dir", required=True, type=str, help="path to directory where the output should be stored")
args = parser.parse_args()

# obtain API key from config file
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=SafeLoader)

OPEN_WEATHER_API_KEY = args.open_weather_api_key
AIRPORTS_FILE_PATH = "../data/iata-icao.csv"
AIRPORTS_LOAD_PATH_FILE = args.airports_load_file
AIRPORTS_DUMP_PATH_DIR = args.airports_dump_dir
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
            logging.info("Open Weather air quality result obtained for " + curr_iata + ": " + str(result["list"][0]["components"]["pm10"]))
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

logging.info("Open Weather air quality data has been obtained")

# assign airports json to local object
with open(AIRPORTS_LOAD_PATH_FILE, "r", encoding="utf-8") as f:
    airports_obj = json.load(f)

# find matching airports and combine data
for airport_a in airports_obj["airports"]:
    # view airport from the airport code data
    iata_a = airport_a["iata"]
    for index in airports_df.index:
        # view airport from the air quality data
        iata_b = airports_df["iata"][index]
        # check for match
        if iata_a == iata_b:
            # if so, transfer air quality data
            airport_a["air_quality"] = float(airports_df["pm10"][index])

# write Python dictionary to json file
with open(AIRPORTS_DUMP_PATH_DIR + "/airports_augmented.json", "w", encoding="utf-8") as f:
    json.dump(airports_obj, f, ensure_ascii=False, indent=4)
