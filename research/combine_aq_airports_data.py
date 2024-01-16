"""
Program to inject air quality data into the airports list from FlightRadar24

IMPORTANT:
- This file must be run AFTER the "open_weather_search.py" file
- This file requires a configuration file to run successfully
- The configuration file must be in the "research" directory and be named "config.yaml"
- The configuration file must at least contain the following:

file_paths:
  airports_load: str (path the JSON file containing information about airports, see below)
  air_quality_load: str (path to air quality measurements obtained from "open_weather_search.py" file)
  airports_augmented_dump: str (path to airport data with air quality measurements now integrated)

airports_load file structure:
{
    airports: [
        {
            “altitude”: int
            “country”: str
            “iata”: str
            “icao”: str
            “name”: str
        },
        {},
        ...
    ]
}
"""

import json
import csv
import yaml
from yaml.loader import SafeLoader

# obtain API key from config file
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=SafeLoader)

AIRPORTS_LOAD_PATH = config["file_paths"]["airports"]
AIR_QUALITY_LOAD_PATH = config["file_paths"]["air_quality"]
AIRPORTS_DUMP_PATH = config["file_paths"]["airports_augmented"]

# assign airports json to local object
with open(AIRPORTS_LOAD_PATH, "r") as f:
    airports_obj = json.load(f)

# assign air quality data to object
air_qualities = []
with open(AIR_QUALITY_LOAD_PATH, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        air_qualities.append(row[0].split("\t"))

# find matching airports and combine data
for airport_a in airports_obj["airports"]:
    # extract airport A
    iata_a = airport_a["iata"]
    for airport_b in air_qualities:
        # extract airport B
        iata_b = airport_b[1]
        # check for match
        if iata_a == iata_b:
            # if so, transfer air quality data
            airport_a["air_quality"] = float(airport_b[5])

# write Python dictionary to json file
with open(AIRPORTS_DUMP_PATH, "w", encoding="utf-8") as f:
    json.dump(airports_obj, f, ensure_ascii=False, indent=4)
