""" Gather flight statistics for each 
    airport from given aiport flight data. 
"""

from dataclasses import dataclass, field
from typing import TypedDict

import pandas as pd


class Flights(TypedDict):
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


@dataclass
class FlightStats:
    flights: pd.DataFrame
    _flight_stats_df: pd.DataFrame = field(init=False)

    def __post_init__(self) -> None:
        self._flight_stats_df = self.flights.map(self.count_flights)
        self._flight_stats_df = pd.DataFrame(
            self._flight_stats_df["flights"].to_list(),
            columns=["total_arrivals", "total_departures"],
        )

    # total arrivals or departures
    def count_flights(self, airport_flights: list[Flights | None]) -> list[int]:
        departures = 0
        arrivals = 0
        if airport_flights:  # if the list is not empty
            airport = airport_flights[0]["origin_iata"]  # type: ignore [index]
            for i in airport_flights:
                if i["origin_iata"] == airport:  # type: ignore [index]
                    departures = departures + 1
                else:
                    arrivals = arrivals + 1
        return [arrivals, departures]

    @property
    def flight_stats_df(self) -> pd.DataFrame:
        return self._flight_stats_df
