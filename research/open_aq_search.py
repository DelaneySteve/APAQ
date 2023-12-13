"""
Testing the OpenAQ API to use a list of airport locations
to search and find air quality measurements within a particular
distance from those locations.
"""

import csv
import pandas as pd
import requests

OPEN_AQ_API_KEY = "d568965fba34916d82780a672e32d0029f0e45f5293dc4f45a1ae33fe827623b"

# -------------------- CONFIG --------------------
lat = "38.9074"         # Latitude [deg]
long = "-77.0373"       # Longitude [deg]
radius = "250"          # Search radius [m]
result_limit = "1000"   # Max number of results returned
# ------------------------------------------------

# Import list of airports and their lat/long locations

# read text file into pandas DataFrame
# airports = pd.read_csv("../data/GlobalAirportDatabase.txt", sep=",")
# print(airports)

with open('../data/GlobalAirportDatabase.txt', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

print(data[1])

for index in range(len(data)):
    current_airport = data[index][0].split(":")
    print(current_airport)


airport = data[0][0].split(":")
print(airport)

lat_degrees = int(airport[5])
lat_minutes = int(airport[6])
lat_seconds = int(airport[7])
lat_direction = airport[8]

lat_dec = float(lat_degrees) + float(lat_minutes)/60 + float(lat_seconds)/(60*60)
if lat_direction == 'E' or lat_direction == 'S':
    lat_dec *= -1
print(lat_dec)

long_degrees = int(airport[9])
long_minutes = int(airport[10])
long_seconds = int(airport[11])
long_direction = airport[12]

long_dec = float(long_degrees) + float(long_minutes)/60 + float(long_seconds)/(60*60)
if long_direction == 'E' or lat_direction == 'S':
    long_dec *= -1
print(long_dec)

data = [airport[2], lat_dec, long_dec]
print(data)


# df = pd.DataFrame(data, columns=["Airport Code", "Latitude", "Longitude"])



# Iterate through each airport's lat/long location and ask the OpenAQ API what
# measurements are within some distance threshold
# if any are found, choose the closest measurement to pair with that airport

url = "https://api.openaq.org/v3/locations?order_by=id&sort_order=asc&coordinates=" + lat + "%2C" + long + "&radius=" + radius + "&limit=" + result_limit + "&page=1"
print(url)
res_json = requests.get(url, headers={"X-API-Key": OPEN_AQ_API_KEY})
res_obj = res_json.json()

# If at least one result was found
results = res_obj["results"]
for result in results:
    print(result["id"], result["name"])
