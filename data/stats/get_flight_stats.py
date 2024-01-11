from dataclasses import dataclass, field
import pandas as pd

@dataclass
class FlightStats:
    flights: list[list[dict|None]] # type: ignore [index]
    flights_count_list: list[dict[str, int | None]] = field(init = False)

    def __post_init__(self) -> None:
        self.flights_count_list = list(map(self.count_flights, self.flights))

    #total arrivals or departures
    def count_flights(self, airport_runways: list[dict|None]) -> dict:
        total: int = len(airport_runways)
        departures: int = 0
        arrivals: int = 0
        flight_data: dict[str, int | None] = {"arrivals": None, "departures": None, "total": None}
        if total != 0:
            airport = airport_runways[0]["origin_iata"] #type: ignore [index]
            for i in airport_runways:
                if i["origin_iata"] == airport: #type: ignore [index]
                    departures = departures + 1
                else:
                    arrivals = arrivals + 1
            flight_data = {"arrivals": arrivals, "departures": departures, "total": total}
        return flight_data

    def flight_count_df(self) -> pd.DataFrame:
        flight_count_df = pd.DataFrame(self.flights_count_list)
        return flight_count_df
    