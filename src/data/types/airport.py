import logging
import time
from dataclasses import dataclass, field
from typing import Any, Literal

import requests

from src.data.types.flight import Flight
from src.data.types.runway import Runway

_logger = logging.getLogger(__name__)


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
    def new_airport(cls, **kwargs: Any) -> 'Airport':
        return Airport(altitude=kwargs['alt'], country=kwargs['country'],
                       iata=kwargs['iata'], icao=kwargs['icao'], name=kwargs['name'])

    def update_runways(self, airport_endpoint: str, headers: dict[str, Any], retry: int = 1) -> None:
        endpoint = f'{airport_endpoint}?code={self.iata}&limit=1'
        _logger.info('Fetching runway information for %s (%s)...', self.name, self.iata)
        resp = requests.get(endpoint, headers=headers, timeout=10)
        if resp.status_code in {429, 502, 503, 504, 520, 529}:
            _logger.error('Error, unexpected response from server: %s (%s)', resp.status_code, resp.reason)
            _logger.info('Retrying request in 2 seconds (attempt %s/5)...', retry)
            time.sleep(2)
            if retry < 5:
                return self.update_runways(airport_endpoint, headers, retry + 1)
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

    def _get_flights(self, endpoint: str, type: Literal['arrivals', 'departures'],
                     headers: dict[str, Any], page_size: int) -> None:
        resp_json = self._fetch_next_page(endpoint, type, headers, page=1)
        self.flights |= self._parse_flights(resp_json['data'], type)

        available_flights = resp_json['item']['total']
        _logger.info('Fetching %s for %s (%s) from %s... '
                     'Page 1/%s', type, self.name, self.iata, endpoint, int(available_flights / page_size) + 1)
        if available_flights > page_size:
            current_flights = page_size
            page = 2
            while available_flights >= current_flights:
                _logger.info('Fetching %s for %s (%s) from %s... '
                             'Page %s/%s', type, self.name, self.iata, endpoint, page, int(available_flights / page_size) + 1)  # pylint: disable=line-too-long
                resp_json = self._fetch_next_page(endpoint, type, headers, page=page)
                self.flights |= self._parse_flights(resp_json['data'], type)
                current_flights += page_size
                page += 1

    def _fetch_next_page(self, endpoint: str, type: Literal['arrivals', 'departures'],
                         headers: dict[str, Any],  page: int, retry: int = 1) -> dict[Any, Any]:
        endpoint = f'{endpoint}&page={page}'
        if page % 7 == 0:
            time.sleep(1.5)
        resp = requests.get(endpoint, headers=headers, timeout=10)
        if resp.status_code == 429:
            print('Unexpected response %s (%s). Request will be retried in 5 seconds...', resp.status_code, resp.reason)
            time.sleep(5)
            self._fetch_next_page(endpoint, type, headers, page)
        elif resp.status_code in {500, 501, 503, 504, 520, 529}:
            _logger.error('Unexpected error response from server: {%s (%s).', resp.status_code, resp.reason)
            if retry < 5:
                _logger.info('The request will be retried in 5 seconds... (retry attempt %s/5)', retry)
                time.sleep(5)
                return self._fetch_next_page(endpoint, type, headers, page, retry + 1)
            resp.raise_for_status()
        elif not resp.status_code == 200:
            _logger.error(resp.status_code)
            resp.raise_for_status()

        return resp.json()['result']['response']['airport']['pluginData']['schedule'][type]

    def _parse_flights(self, flights_data: list[dict[str, Any]], type: Literal['arrivals', 'departures']) -> set[Flight]:  # pylint: disable=(line-too-long
        is_arrival = type == 'arrivals'
        return {Flight.new_flight(self.iata, self.icao, flight_data=flight, is_arrival=is_arrival) for flight in flights_data}  # pylint: disable=(line-too-long

    def json(self) -> dict[str, str | int | list[dict[str, str | int]]]:
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
        values: list[str | int] = [self.altitude, self.country, self.iata, self.icao, self.name]
        return columns, values
