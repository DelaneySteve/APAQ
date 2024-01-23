""" Gather runway statistics for each 
    airport from given airport runway data. 
"""

from dataclasses import dataclass, field
from typing import TypedDict

import pandas as pd


class Runways(TypedDict):
    length_in_ft: int
    length_in_m: int
    name: str
    surface: str


@dataclass
class RunwayStats:
    runways: pd.DataFrame
    _runways_stats_df: pd.DataFrame = field(init=False)

    def __post_init__(self) -> None:
        self._runways_stats_df = pd.DataFrame(self.runways.map(self.count_runways))
        self._runways_stats_df["total_runway_length"] = pd.DataFrame(
            self.runways.map(self.sum_runways_len)
        )

    def count_runways(self, airport_runways: list[Runways | None]) -> int | None:
        return len(airport_runways) or None

    def sum_runways_len(self, airport_runways: list[Runways | None]) -> int | None:
        return sum(runway["length_in_ft"] for runway in airport_runways) or None  # type: ignore [index]

    @property
    def runways_stats_df(self) -> pd.DataFrame:
        return self._runways_stats_df
