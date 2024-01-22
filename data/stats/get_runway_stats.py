"""
    Gather runway statistics for each 
    airport from given airport runway data. 
"""

from dataclasses import dataclass, field
import pandas as pd
from src.data.types import Runway

@dataclass
class RunwayStats:
    runways: pd.DataFrame
    count: pd.DataFrame = field(init=False)
    len: pd.DataFrame = field(init = False)

    def __post_init__(self) -> None:
        self.count = pd.DataFrame(self.runways.map(self.count_runways))
        self.len = pd.DataFrame(self.runways.map(self.sum_runways_len))

    def count_runways(self, airport_runways: list[Runway|None]) -> int | None:
        runway_counter: int|None
        runway_counter = len(airport_runways)
        if runway_counter == 0:
            runway_counter = None
        return runway_counter

    def sum_runways_len(self, airport_runways: list[Runway|None]) -> int | None:
        if airport_runways:  #if the list is not empty
            total_runway_length = 0
            for i in airport_runways:
                temp_len = i["length_in_ft"] #type: ignore [index]
                total_runway_length = total_runway_length + temp_len
                return total_runway_length
        return None

    def runway_df(self) -> pd.DataFrame:
        runways_df = self.count
        runways_df["total_runway_length"] = self.len
        return runways_df
