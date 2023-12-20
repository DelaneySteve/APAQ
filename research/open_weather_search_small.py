"""
Testing the IQAir API to use a list of airport locations
to search and find air quality measurements within a particular
distance from those locations.
"""

import csv
import pandas as pd
import requests

# IQAIR_API_KEY = "6de120c9-2864-4603-ac6b-28a56ecd5837"
OPEN_WEATH_API_KEY = "a6fa40646975e01954d98e207db40b18"

# url = "http://api.airvisual.com/v2/nearest_city?lat=" + str(lat) + "&lon=" + str(lon) + "&key={IQAIR_API_KEY}"
# url =f"http://api.airvisual.com/v2/countries?key={IQAIR_API_KEY}"


def long_lat_conv(degrees: int, minutes: int, seconds: int, direction: str) -> float:
    """
    Convert longitude or latitude from degrees, minutes, seconds, and direction to 
    a decimal value.
    
    Return: float

    """
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'W' or direction == 'S':
        dd *= -1
    return dd


# Import list of airports and their lat/long locations
with open("../data/GlobalAirportDatabase.txt", newline="") as f:
    reader = csv.reader(f)
    data = list(reader)

airport_codes = []
airport_lats = []
airport_lons = []
airport_pm10s = []

for index in range(len(data)):
    curr_airport = data[index][0].split(":")
    if "N/A" not in curr_airport:
        curr_icao = curr_airport[0]
        curr_lat = long_lat_conv(int(curr_airport[5]), int(curr_airport[6]), int(curr_airport[7]), curr_airport[8])
        curr_lon = long_lat_conv(int(curr_airport[9]), int(curr_airport[10]), int(curr_airport[11]), curr_airport[12])

        url = "http://api.openweathermap.org/data/2.5/air_pollution?lat=" + str(curr_lat) + "&lon=" + str(curr_lon) + "&appid=" + OPEN_WEATH_API_KEY

        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            # Process 'result' as needed
            try:
                airport_pm10s.append(float(result["list"][0]["components"]["pm10"]))
                airport_codes.append(curr_icao)
                airport_lats.append(curr_lat)
                airport_lons.append(curr_lon)
                print(str(round((index / len(data)) * 100, 1)) + "%", curr_icao, curr_lat, curr_lon, flush=True)

            except KeyError:
                curr_pm10 = None
        else:
            print("Request failed with status code:", response.status_code)

airports_df = pd.DataFrame({
                            "icao": airport_codes,
                            "latitude": airport_lats,
                            "longitude": airport_lons,
                            "pm10": airport_pm10s
                            })
print(airports_df)

airports_df.to_csv("airports_aq_small.csv", sep='\t')
