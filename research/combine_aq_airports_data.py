"""
Program to inject air quality data into the airports list from FlightRadar24
"""

import json
import csv

# assign airports json to local object
with open("../data/airports.json", "r") as f:
    airports_orig = json.load(f)

# assign air quality data to object
air_qualities = []
with open("../data/airports_aq_large.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        air_qualities.append(row[0].split("\t"))

# new object to store augmented airports list in
airports_augmented = {"airports": []}

# find matching airports and combine data
for airport_a in airports_orig["airports"]:
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
with open("../data/airports_augmented.json", "w", encoding="utf-8") as f:
    json.dump(airports_orig, f, ensure_ascii=False, indent=4)
