import json
import random
from random import randint
from typing import Any

import pandas as pd
from faker import Faker
from faker_airtravel import AirTravelProvider  # type: ignore[import-untyped]

fake = Faker()
fake.add_provider(AirTravelProvider)

MAX_ALTITUDE = 13325
MAX_RUNWAY_FT = 1000.0
MAX_RUNWAY_M = 500.0
MIN_RUNWAY_FT = 200.0
MIN_RUNWAY_M = 100.0
MAX_NUMBER_FLIGHTS = 500
MAX_NUMBER_RUNWAYS = 16

DATA_PATH = 'data/tests/model_test_subset_dataset.json'
NUM_SAMPLES = 20

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)
airports_df = pd.DataFrame(raw_data['airports'])


def get_item_from_airport_list(column_name: str) -> Any:
    list_from_airports = airports_df[column_name]
    return random.choice(list_from_airports)


def get_item_from_flight_runway_list(column_name: str, list_type: str) -> Any:
    flights = airports_df[list_type]
    if flights:
        random_airport = random.choice(flights)
        if random_airport:
            random_flight = random.choice(random_airport)
            return random_flight[column_name]
    return None


def fake_airports_generator(length: int) -> list[dict[str, Any]]:
    airports_list = []
    for _ in range(length):
        fake_airport = fake.airport_object()
        og_iata = fake_airport['iata']
        og_icao = fake_airport['icao']
        altitude = get_item_from_airport_list('altitude')
        airport = {
            'altitude': int(altitude),
            'country': fake_airport['country'],
            'flights': fake_flight_list(randint(0, MAX_NUMBER_FLIGHTS), og_iata, og_icao),
            'iata': og_iata,
            'icao': og_icao,
            'name': fake_airport['airport'],
            'runways': fake_runway_list(randint(0, MAX_NUMBER_RUNWAYS)),
            'air_quality': altitude / 100
        }
        airports_list.append(airport)
    return airports_list


def fake_flight_list(length: int, og_iata: str, og_icao: str) -> list[dict[str, Any]]:
    flight_list = []
    for _ in range(length):
        sched_arrival = get_item_from_flight_runway_list('scheduled_arrival', 'flights')
        sched_departure = get_item_from_flight_runway_list('scheduled_departure', 'flights')
        sched_arrival = int(sched_arrival) if sched_arrival else None
        sched_departure = int(sched_departure) if sched_departure else None
        flight = {
            'aircraft_model': get_item_from_flight_runway_list('aircraft_model', 'flights'),
            'airline': fake.airline(),
            'destination_iata': fake.airport_iata() if randint(0, 10) > 3 else og_iata,
            'destination_icao': fake.airport_icao() if randint(0, 10) > 3 else og_icao,
            'flight_number': get_item_from_flight_runway_list('flight_number', 'flights'),
            'long_aircraft_name': get_item_from_flight_runway_list('long_aircraft_name', 'flights'),
            'origin_iata': og_iata if randint(0, 10) > 3 else fake.airport_iata(),
            'origin_icao': og_icao if randint(0, 10) > 3 else fake.airport_icao(),
            'scheduled_arrival': sched_arrival,
            'scheduled_departure': sched_departure
        }
        flight_list.append(flight)
    return flight_list


def fake_runway_list(length: int) -> list[dict[str, Any]]:
    runway_list = []
    for _ in range(length):
        length_in_ft = get_item_from_flight_runway_list('length_in_ft', 'runways')
        length_in_m = 0.3048 * length_in_ft if length_in_ft else None
        runway = {
            'length_in_ft': length_in_ft,
            'length_in_m': length_in_m,
            'name': get_item_from_flight_runway_list('name', 'runways'),
            'surface': get_item_from_flight_runway_list('surface', 'runways')
        }
        runway_list.append(runway)
    return runway_list


if __name__ == '__main__':
    airports = {'airports': fake_airports_generator(NUM_SAMPLES)}

    with open('data/tests/mock_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(airports, f, indent=4)
