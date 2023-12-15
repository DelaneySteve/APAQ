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
radius = "1600"          # Search radius [m]
loc_result_limit = "100"   # Max number of location results returned
measurement_result_limit = "10"  # max number of measurement results returned for a location (for some reason <=2 causes a 402 timeout)
# ------------------------------------------------

def long_lat_conv(degrees: int, minutes: int, seconds: int, direction: str) -> float:
    """
    Convert longitude or latitude from degrees, minutes, seconds, and direction to 
    a decimal value.
    
    Return: float

    """
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'E' or direction == 'S':
        dd *= -1
    return dd


# Import list of airports and their lat/long locations

# read text file into pandas DataFrame
# airports = pd.read_csv("../data/GlobalAirportDatabase.txt", sep=",")
# print(airports)

with open("../data/GlobalAirportDatabase.txt", newline="") as f:
    reader = csv.reader(f)
    data = list(reader)

print(data[1])

airports_list = []

for index in range(len(data)):
    curr_airport = data[index][0].split(":")
    curr_name = curr_airport[2]
    if curr_name != "N/A":
        curr_lat = long_lat_conv(int(curr_airport[5]), int(curr_airport[6]), int(curr_airport[7]), curr_airport[8])
        curr_long = long_lat_conv(int(curr_airport[9]), int(curr_airport[10]), int(curr_airport[11]), curr_airport[12])
        airports_list.append([curr_name, curr_lat, curr_long])

print(airports_list[0])

airports_df = pd.DataFrame(airports_list, columns=["Airport Name", "Latitude", "Longitude"])
print(airports_df)

# Iterate through each airport's lat/long location and ask the OpenAQ API what
# measurements are within some distance threshold
# if any are found, choose the closest measurement THAT ALSO has a PM10 parameter
# to associate to that airport

# aq_measurements = []
# for index, row in airports_df.iterrows():
#     curr_url = "https://api.openaq.org/v3/locations?order_by=id&sort_order=asc&coordinates=" + str(row['Latitude']) + "%2C" + str(row['Longitude']) + "&radius=" + radius + "&limit=" + result_limit + "&page=1"
#     res_json = requests.get(curr_url, headers={"X-API-Key": OPEN_AQ_API_KEY})
#     res_obj = res_json.json()


loc_url = "https://api.openaq.org/v3/locations?order_by=id&sort_order=asc&coordinates=" + lat + "%2C" + long + "&radius=" + radius + "&limit=" + loc_result_limit + "&page=1"
print(loc_url)
loc_res_json = requests.get(loc_url, headers={"X-API-Key": OPEN_AQ_API_KEY})
loc_res_obj = loc_res_json.json()

# If at least one result was found
loc_results = loc_res_obj["results"]
# print("x->", loc_results)
pm10_list = []
cumulative_sum_pm10 = 0
num_measurements_pm10 = 0
for loc_result in loc_results:
    curr_id = loc_result["id"]
    curr_name = loc_result["name"]
    print(curr_name, curr_id)

    curr_measurement_url = "https://api.openaq.org/v3/locations/" + str(curr_id) + "/measurements?period_name=hour&limit=" + measurement_result_limit + "&page=1"
    measurement_res_json = requests.get(curr_measurement_url, headers={"X-API-Key": OPEN_AQ_API_KEY})
    measurement_res_obj = measurement_res_json.json()
    if "detail" not in measurement_res_obj:
        measurement_results = measurement_res_obj["results"]
        # Search for PM10
        for measurement_result in measurement_results:
            if measurement_result["parameter"]["name"] == "pm10":
                # If has PM10, record the distance and value
                cumulative_sum_pm10 += measurement_result["value"]
                num_measurements_pm10 += 1
                pm10_list.append([curr_name, measurement_result["value"]])

        print("z->", pm10_list)

if num_measurements_pm10 > 0:
    pm10_avg = cumulative_sum_pm10 / num_measurements_pm10
    print(pm10_avg)


