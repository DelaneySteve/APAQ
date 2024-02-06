import argparse
import json
import sys
import time
import traceback

import requests

from src.utils import setup_logger
from src.data.types import Airport, Flight, Runway

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
                        help='If provided, airport information will be loaded from the specified file. '
                             'Note: the file must be valid JSON.')
    parser.add_argument('--update-runways', action='store_true',
                        help='Use this flag to update the available runways for all airports in specified airports dataset, '  # pylint: disable=line-too-long
                             'or to fetch runway details when fetching airports.')
    parser.add_argument('--get-flights', action='store_true',
                        help='When set flights for all airports specified will be retrieved and saved.')

    return parser


def get_all_airports() -> list[Airport]:
    resp = requests.get(AIRPORTS_ENDPOINT, headers=REQUEST_HEADERS, timeout=10)
    airports = []
    for airport in resp.json()['rows']:
        airports.append(Airport.new_airport(**airport))
    return airports


def load_airports(file_name: str) -> list[Airport]:
    with open(file_name, 'r', encoding='utf-8') as f:
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
        if len(airport.flights) > 1:
            logger.info('Flights already exist for %s (%s)), skipping...', airport.name, airport.iata)
            continue
        try:
            airport.get_flights(FLIGHTS_ENDPOINT, REQUEST_HEADERS, 100)
            time.sleep(1.8)
        except Exception:  # pylint: disable=broad-exception-caught
            logger.critical(traceback.format_exc())
            logger.error('An error occurred when retrieving flight information for %s (%s).\n'
                         'Airport index %s', airport.name, airport.iata, idx)
            return


def get_runways(airports: list[Airport]) -> None:
    for idx, airport in enumerate(airports):
        if len(airport.runways) > 1:
            continue
        try:
            airport.update_runways(FLIGHTS_ENDPOINT, REQUEST_HEADERS)
            time.sleep(0.6)
        except Exception:   # pylint: disable=broad-exception-caught
            logger.critical(traceback.format_exc())
            logger.error('An error occurred when retrieving runway information for %s (%s).\n'
                         'Airport index %s', airport.name, airport.iata, idx)
            return


def save_airports(airports: list[Airport]) -> None:
    airports_json = {'airports': [airport.json() for airport in airports]}
    logger.info('Saving updated flights data to "airports.json"')
    with open('airports.json', 'w', encoding='utf-8') as f:
        json.dump(airports_json, f, indent=4, ensure_ascii=False, sort_keys=True)


def main(args: list[str]) -> None:
    parser = setup_parser()
    args = parser.parse_args(args)
    airports = []
    if (args.get_airports and args.airports_dataset) or (not args.get_airports and not args.airports_dataset):
        raise ValueError('Exactly one of `--get-airports` and `--airports-dataset` must of specified.')

    if args.airports_dataset:
        logger.info('Loading airports and flight information from %s...', args.airports_dataset)
        airports = load_airports(args.airports_dataset)
        logger.info('Loaded airports and flight information from %s.', args.airports_dataset)
    elif args.get_airports:
        logger.info('Fetching a list of all global airports from %s...', AIRPORTS_ENDPOINT)
        airports = get_all_airports()

    if args.update_runways:
        get_runways(airports)
    if args.get_flights:
        get_flights(airports)

    save_airports(airports)


if __name__ == '__main__':
    main(sys.argv[1:])
