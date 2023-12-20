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
radius = "10000"          # Search radius [m]
loc_result_limit = "1"   # Max number of location results returned
measurement_result_limit = "10"  # max number of measurement results returned for a location (for some reason <=2 causes a 402 timeout)
# ------------------------------------------------

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
        print(str(round((index / len(data)) * 100, 1)) + "%", curr_name, curr_lat, curr_long, flush=True)

        loc_url = "https://api.openaq.org/v3/locations?order_by=id&sort_order=asc&coordinates=" + str(curr_lat) + "%2C" + str(curr_long) + "&radius=" + radius + "&limit=" + loc_result_limit + "&page=1"
        loc_res_json = requests.get(loc_url, headers={"X-API-Key": OPEN_AQ_API_KEY})
        loc_res_obj = loc_res_json.json()

        # If at least one result was found
        if "results" in loc_res_obj:
            loc_results = loc_res_obj["results"]
            # print("x->", loc_results)
            pm10_list = []
            cumulative_sum_pm10 = 0
            num_measurements_pm10 = 0
            for loc_result in loc_results:
                curr_id = loc_result["id"]
                curr_name = loc_result["name"]
                curr_measurement_url = "https://api.openaq.org/v3/locations/" + str(curr_id) + "/measurements?period_name=hour&limit=" + measurement_result_limit + "&page=1"
                measurement_res_json = requests.get(curr_measurement_url, headers={"X-API-Key": OPEN_AQ_API_KEY})
                measurement_res_obj = measurement_res_json.json()
                if "results" in measurement_res_obj:
                    measurement_results = measurement_res_obj["results"]
                    # Search for PM10
                    for measurement_result in measurement_results:
                        if measurement_result["parameter"]["name"] == "pm10":
                            print("---", measurement_result["value"])
                            # If has PM10, record the distance and value
                            cumulative_sum_pm10 += measurement_result["value"]
                            num_measurements_pm10 += 1
                            pm10_list.append([curr_name, measurement_result["value"]])

            if num_measurements_pm10 > 0:
                pm10_avg = cumulative_sum_pm10 / num_measurements_pm10            
                airports_list.append([curr_name, curr_lat, curr_long, pm10_avg])

        elif "details" in loc_res_obj:
            print("-->", loc_res_obj["details"], flush=True)
        
        else:
            print("--> Other", flush=True)
            

print(airports_list[0])

airports_df = pd.DataFrame(airports_list, columns=["Airport Name", "Latitude", "Longitude", "PM10"])
print(airports_df)

airports_df.to_csv("airports_pm10.csv", index=True)
