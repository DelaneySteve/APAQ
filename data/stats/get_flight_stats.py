"""
    Gather flight statistics for each 
    airport from given aiport flight data. 
"""

from dataclasses import dataclass, field
import pandas as pd
from src.data.types import Flight

@dataclass
class FlightStats:
    flights: pd.DataFrame
    flights_count_list: pd.DataFrame = field(init = False)
    def __post_init__(self) -> None:
        self.flights_count_list = self.flights.map(self.count_flights)

    #total arrivals or departures
    def count_flights(self, airport_flights: list[Flight|None]) -> list[int]:
        total: int = len(airport_flights)
        departures: int = 0
        arrivals: int = 0
        if total != 0: #if the list is not empty
            airport = airport_flights[0]["origin_iata"] #type: ignore [index]
            for i in airport_flights:
                if i["origin_iata"] == airport: #type: ignore [index]
                    departures = departures + 1
                else:
                    arrivals = arrivals + 1
        return [arrivals, departures, total]

    def flight_count_df(self) -> pd.DataFrame:
        flight_count_df = pd.DataFrame(self.flights_count_list["flights"].to_list(),
                                       columns=["total_arrivals", "total_departures", "total"])
        return flight_count_df
    