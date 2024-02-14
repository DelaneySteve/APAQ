import json
from random import randint, uniform
from typing import Any

from faker import Faker
from faker_airtravel import AirTravelProvider

fake = Faker()
fake.add_provider(AirTravelProvider)

MAX_ALTITUDE = 13325
MAX_RUNWAY_FT = 1000.0
MAX_RUNWAY_M = 500.0
MIN_RUNWAY_FT = 200.0
MIN_RUNWAY_M = 100.0
MAX_NUMBER_FLIGHTS = 500
MAX_NUMBER_RUNWAYS = 16
MAX_NUMBER_AIRPORTS = 100


def fake_airports_generator(length: int) -> list[dict[str, Any]]:
    airports_list = []
    for _ in range(length):  # xrange in Python 2.7
        og_iata = fake.airport_iata()
        og_icao = fake.airport_icao()
        altitude = randint(0, MAX_ALTITUDE)
        airport = {
            'altitude': altitude,
            'country': fake.country(),
            'flights': fake_flight_list(randint(0, MAX_NUMBER_FLIGHTS), og_iata, og_icao),
            'iata': og_iata,
            'icao': og_icao,
            'name': fake.airport_name(),
            'runways': fake_runway_list(randint(0, MAX_NUMBER_RUNWAYS)),
            'air_quality': altitude / 100
        }
        airports_list.append(airport)
    return airports_list


def fake_flight_list(length: int, og_iata: str, og_icao: str) -> list[dict[str, Any]]:
    flight_list = []
    for _ in range(length):  # xrange in Python 2.7
        if randint(0, 10) > 3:  # set to og_iata
            flight = {
                'aircraft_model': uniform(0, 100),
                'airline': fake.airline(),
                'destination_iata': fake.airport_iata(),
                'destination_icao': fake.airport_icao(),
                'flight_number': 'ABCD',
                'long_aircraft_name': ' ',
                'origin_iata': og_iata,
                'origin_icao': og_icao,
                'scheduled_arrival': randint(1700000000, 1800000000),
                'scheduled_departure': randint(1700000000, 1800000000) 
            }
        else:  # set to random origin iata
            flight = {
                'aircraft_model': uniform(0, 100),
                'airline': fake.airline(),
                'destination_iata': og_iata,
                'destination_icao': og_icao,
                'flight_number': 'ABCD',
                'long_aircraft_name': ' ',
                'origin_iata': fake.airport_iata(),
                'origin_icao': fake.airport_icao(),
                'scheduled_arrival': randint(1700000000, 1800000000),
                'scheduled_departure': randint(1700000000, 1800000000) 
            }
        flight_list.append(flight)
    return flight_list


def fake_runway_list(length: int) -> list[dict[str, Any]]:
    runway_list = []
    for _ in range(length):  # xrange in Python 2.7
        runway = {
            'length_in_ft': uniform(MIN_RUNWAY_FT, MAX_RUNWAY_FT),
            'length_in_m': uniform(MIN_RUNWAY_M, MAX_RUNWAY_M),
            'name': 'fakename',
            'surface': 'fakesurface'
        }
        runway_list.append(runway)
    return runway_list


airports = {'airports': fake_airports_generator(MAX_NUMBER_AIRPORTS)}

with open('data/tests/fake_data.json', 'w', encoding='utf-8') as f:
    json.dump(airports, f, indent=4)
