import argparse
import json
import sys
import time
import traceback

import requests

from src.flightradar_data.utils import setup_logger
from src.flightradar_data.types import Airport, Flight, Runway

logger = setup_logger()


REQUEST_HEADERS = {
    'user-agent': 'Chrome/120.0.6099.129'
}
FLIGHTS_ENDPOINT = 'https://api.flightradar24.com/common/v1/airport.json'
AIRPORTS_ENDPOINT = 'https://www.flightradar24.com/_json/airports.php'


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Configuration for retrieving and processing FlightRadar24 data')
    parser.add_argument('--get-airports', action='store_true',
                        help='Use this flag to retrieve and save a list of all global airports.')
    parser.add_argument('--airports-dataset', type=str,
                        help='If provided, airport information will be loaded from the specified file. Note: the file must be valid JSON.')
    parser.add_argument('--update-runways', action='store_true',
                        help='Use this flag to update the available runways for all airports in specified airports dataset, '
                             'or to fetch runway details when fetching airports.')
    parser.add_argument('--get-flights', action='store_true',
                        help='When set flights for all airports specified will be retrieved and saved.')

    return parser


def get_all_airports() -> list[Airport]:
    resp = requests.get(AIRPORTS_ENDPOINT, headers=REQUEST_HEADERS)
    airports = []
    for airport in resp.json()['rows']:
        airports.append(Airport.new_airport(**airport))
    return airports


def load_airports(file_name: str) -> list[Airport]:
    with open(file_name, 'r') as f:
        contents = json.load(f)
    if not isinstance(contents, dict) or 'airports' not in contents or not isinstance(contents['airports'], list):
        raise ValueError(f'The file {file_name!r} is improperly formatted.')
    airports = []
    for airport in contents['airports']:
        flights_set = {Flight(**flight) for flight in airport.pop('flights')}
        runways_set = {Runway(**runway) for runway in airport.pop('runways')}
        airports.append(Airport(**airport, flights=flights_set, runways=runways_set))
    return airports


def get_flights(airports: list[Airport]) -> None:
    for idx, airport in enumerate(airports):
        try:
            airport.get_flights(FLIGHTS_ENDPOINT, REQUEST_HEADERS, 100)
            time.sleep(1.8)
        except Exception:
            logger.critical(traceback.format_exc())
            logger.error(f'An error occurred when retrieving flight information for {airport.name} ({airport.iata}).\n'
                         f'Airport index {idx}')
            return


def get_runways(airports: list[Airport]) -> None:
    for idx, airport in enumerate(airports):
        if len(airport.runways) > 1:
            continue
        try:
            airport.update_runways(FLIGHTS_ENDPOINT, REQUEST_HEADERS)
            time.sleep(0.6)
        except Exception:
            logger.critical(traceback.format_exc())
            logger.error(f'An error occurred when retrieving runway information for {airport.name} ({airport.iata}).\n'
                         f'Airport index {idx}')
            return


def save_airports(airports: list[Airport]) -> None:
    airports_json = {'airports': [airport.json() for airport in airports]}
    logger.info('Saving updated flights data to "airports.json"')
    with open('airports.json', 'w') as f:
        json.dump(airports_json, f, indent=4, ensure_ascii=False, sort_keys=True)


def main(args: list[str]) -> None:
    parser = setup_parser()
    args = parser.parse_args(args)
    airports = []
    if (args.get_airports and args.airports_dataset) or (not args.get_airports and not args.airports_dataset):
        raise ValueError('Exactly one of `--get-airports` and `--airports-dataset` must of specified.')

    if args.airports_dataset:
        logger.info(f'Loading airports and flight information from {args.airports_dataset!r}...')
        airports = load_airports(args.airports_dataset)
        logger.info(f'Loaded airports and flight information from {args.airports_dataset!r}.')
    elif args.get_airports:
        logger.info(f'Fetching a list of all global airports from {AIRPORTS_ENDPOINT!r}...')
        airports = get_all_airports()

    if args.update_runways:
        get_runways(airports)
    if args.get_flights:
        get_flights(airports)

    save_airports(airports)


if __name__ == '__main__':
    main(sys.argv[1:])
