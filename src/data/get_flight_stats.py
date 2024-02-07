''' Gather flight statistics for each 
    airport from given aiport flight data. 
'''

from dataclasses import InitVar, dataclass, field
from typing import TypedDict

import pandas as pd


class FlightDict(TypedDict):
    aircraft_model: str | None
    airline: str | None
    destination_iata: str | None
    destination_icao: str | None
    flight_number: str
    long_aircraft_name: str | None
    origin_iata: str | None
    origin_icao: str | None
    scheduled_arrival: int
    scheduled_departure: int


@dataclass
class FlightStats:
    flights: InitVar[pd.DataFrame]
    _flight_stats_df: pd.DataFrame = field(init=False)

    def __post_init__(self, flights: pd.DataFrame) -> None:
        self._flight_stats_df = flights.map(self.count_flights)
        self._flight_stats_df = pd.DataFrame(
            self._flight_stats_df['flights'].to_list(),
            columns=['total_arrivals', 'total_departures'],
        )

    # total arrivals or departures
    def count_flights(self, airport_flights: list[FlightDict]) -> list[int]:
        departures = 0
        arrivals = 0
        if airport_flights:  # if the list is not empty
            airport = airport_flights[0]['origin_iata']
            for flight in airport_flights:
                if flight['origin_iata'] == airport:
                    departures = departures + 1
                else:
                    arrivals = arrivals + 1
        return [arrivals, departures]

    @property
    def flight_stats_df(self) -> pd.DataFrame:
        return self._flight_stats_df
