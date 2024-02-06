""" Gather runway statistics for each 
    airport from given airport runway data. 
"""

from dataclasses import InitVar, dataclass, field
from typing import TypedDict

import pandas as pd


class RunwayDict(TypedDict):
    length_in_ft: int
    length_in_m: int
    name: str
    surface: str


@dataclass
class RunwayStats:
    runways: InitVar[pd.DataFrame]
    _runways_stats_df: pd.DataFrame = field(init=False)

    def __post_init__(self, runways: pd.DataFrame) -> None:
        self._runways_stats_df = runways.map(self.count_runways)
        self._runways_stats_df["total_runway_length"] = runways.map(self.sum_runways_len)

    def count_runways(self, airport_runways: list[RunwayDict]) -> int | None:
        return len(airport_runways) or None

    def sum_runways_len(self, airport_runways: list[RunwayDict]) -> int | None:
        return sum(runway["length_in_ft"] for runway in airport_runways) or None

    @property
    def runways_stats_df(self) -> pd.DataFrame:
        return self._runways_stats_df
