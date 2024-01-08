import logging
import time
import traceback
from dataclasses import dataclass, field
from typing import Any, Literal

import requests


_logger = logging.getLogger(__name__)


@dataclass(unsafe_hash=True)
class Flight:
    aircraft_model: str
    airline: str
    destination_iata: str
    destination_icao: str
    flight_number: str
    long_aircraft_name: str
    origin_iata: str
    origin_icao: str
    scheduled_arrival: int
    scheduled_departure: int

    @classmethod
    def new_flight(cls, airport_iata: str, airport_icao: str, /, *, flight_data: dict[str, Any],
                   is_arrival: bool) -> 'Flight':
        flight_info = flight_data['flight']
        if is_arrival:
            origin_info = flight_info['airport']['origin']
            origin_iata = None if not origin_info else origin_info['code']['iata']
            origin_icao = None if not origin_info else origin_info['code']['icao']
            destination_iata = airport_iata
            destination_icao = airport_icao
        else:
            destination_info = flight_info['airport']['destination']
            destination_iata = None if not destination_info else destination_info['code']['iata']
            destination_icao = None if not destination_info else destination_info['code']['icao']
            origin_iata = airport_iata
            origin_icao = airport_icao

        airline = None if not flight_info['airline'] else flight_info['airline']['name']
        aircraft_model = None if not flight_info['aircraft'] else flight_info['aircraft']['model']['code']
        aircraft_long_name = None if not flight_info['aircraft'] else flight_info['aircraft']['model']['text']
        try:
            return Flight(
                aircraft_model=aircraft_model,
                airline=airline,
                destination_iata=destination_iata,
                destination_icao=destination_icao,
                flight_number=flight_info['identification']['number']['default'],
                long_aircraft_name=aircraft_long_name,
                origin_iata=origin_iata,
                origin_icao=origin_icao,
                scheduled_arrival=flight_info['time']['scheduled']['arrival'],
                scheduled_departure=flight_info['time']['scheduled']['departure']
            )
        except TypeError as e:
            _logger.critical(traceback.format_exc())
            _logger.error(flight_info)

    def json(self) -> dict[str, str | int]:
        return self.__dict__

    def csv(self) -> tuple[list[str], list[str | int]]:
        return list(self.__dict__.keys()), list(self.__dict__.values())


@dataclass(unsafe_hash=True)
class Runway:
    name: str
    length_in_m: int
    length_in_ft: int
    surface: str

    @classmethod
    def new_runway(cls, runway_info: dict[str, Any]) -> 'Runway':
        return Runway(
            name=runway_info['name'],
            length_in_m=runway_info['length']['m'],
            length_in_ft=runway_info['length']['ft'],
            surface=runway_info['surface']['name']
        )

    def json(self) -> dict[str, str | int]:
        return self.__dict__


@dataclass
class Airport:
    country: str
    altitude: int
    iata: str
    icao: str
    name: str
    flights: set[Flight] = field(default_factory=set, compare=False)
    runways: set[Runway] = field(default_factory=set)

    @classmethod
    def new_airport(cls, **kwargs) -> 'Airport':
        return Airport(altitude=kwargs['alt'], country=kwargs['country'], iata=kwargs['iata'], icao=kwargs['icao'],
                       name=kwargs['name'])

    def update_runways(self, airport_endpoint: str, headers: dict[str, Any], retry: int = 1) -> None:
        endpoint = f'{airport_endpoint}?code={self.iata}&limit=1'
        _logger.info(f'Fetching runway information for {self.name} ({self.iata})...')
        resp = requests.get(endpoint, headers=headers)
        if resp.status_code in (429, 502, 503, 504, 520, 529):
            _logger.error(f'Error, unexpected response from server: {resp.status_code} ({resp.reason})')
            _logger.info(f'Retrying request in 2 seconds (attempt {retry}/5)...')
            time.sleep(2)
            if retry < 5:
                self.update_runways(airport_endpoint, headers, retry + 1)
            else:
                resp.raise_for_status()
        if not resp.status_code == 200:
            resp.raise_for_status()
        runway_info = resp.json()['result']['response']['airport']['pluginData']['runways'] or []
        self.runways |= {Runway.new_runway(runway) for runway in runway_info}

    def get_flights(self, flights_endpoint: str, headers: dict[str, Any], page_size: int = 100) -> None:
        endpoint = f'{flights_endpoint}?code={self.iata}&limit={page_size}'
        self._get_flights(endpoint, 'arrivals', headers, page_size)
        self._get_flights(endpoint, 'departures', headers, page_size)

    def _get_flights(self, endpoint: str, type: Literal['arrivals', 'departures'], headers: dict[str, Any], page_size: int) -> None:
        resp_json = self._fetch_next_page(endpoint, type, headers, page=1)
        self.flights |= self._parse_flights(resp_json['data'], type)

        available_flights = resp_json['item']['total']
        _logger.info(f'Fetching {type} for {self.name} ({self.iata}) from {endpoint!r}... '
                     f'Currently on page 1/{int(available_flights / page_size) + 1}')
        if available_flights > page_size:
            current_flights = page_size
            page = 2
            while available_flights >= current_flights:
                _logger.info(f'Fetching {type} for {self.name} ({self.iata}) from {endpoint!r}... '
                             f'Currently on page {page}/{int(available_flights/page_size) + 1}')
                resp_json = self._fetch_next_page(endpoint, type, headers, page=page)
                self.flights |= self._parse_flights(resp_json['data'], type)
                current_flights += page_size
                page += 1

    def _fetch_next_page(self, endpoint: str, type: Literal['arrivals', 'departures'], headers: dict[str, Any], page: int, retry: int = 1) -> dict[Any, Any]:
        endpoint = f'{endpoint}&page={page}'
        if page % 7 == 0:
            time.sleep(1.5)
        resp = requests.get(endpoint, headers=headers)
        if resp.status_code == 429:
            print(f'Unexpected response {resp.status_code} ({resp.reason}). Request will be retried in 10 seconds...')
            time.sleep(10)
            self._fetch_next_page(endpoint, type, headers, page)
        elif resp.status_code in (500, 501, 503, 504, 520, 529):
            _logger.error(f'Unexpected error response from server: {resp.status_code} ({resp.reason}).')
            if retry < 5:
                _logger.info(f'The request will be retried in 5 seconds... (retry attempt {retry}/5)')
                time.sleep(5)
                return self._fetch_next_page(endpoint, type, headers, page, retry + 1)
            resp.raise_for_status()
        elif not resp.status_code == 200:
            _logger.error(resp.status_code)
            resp.raise_for_status()

        return resp.json()['result']['response']['airport']['pluginData']['schedule'][type]

    def _parse_flights(self, flights_data: list[dict[str, Any]], type: Literal['arrivals', 'departures']) -> set[Flight]:
        is_arrival = type == 'arrivals'
        return {Flight.new_flight(self.iata, self.icao, flight_data=flight, is_arrival=is_arrival) for flight in flights_data}

    def json(self) -> dict[str, str | int | dict[str, str | int]]:
        return {
            'altitude': self.altitude,
            'country': self.country,
            'flights': [flight.json() for flight in self.flights],
            'iata': self.iata,
            'icao': self.icao,
            'name': self.name,
            'runways': [runway.json() for runway in self.runways]
        }

    def csv(self) -> tuple[list[str], list[str | int]]:
        columns = ['altitude', 'country', 'iata', 'icao', 'name']
        values = [self.altitude, self.country, self.iata, self.icao, self.name]
        return columns, values
