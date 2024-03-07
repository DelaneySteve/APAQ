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
        runways_count = list(map(self.count_runways, runways['runways'], runways['iata']))
        runways_length = list(map(self.sum_runways_len, runways['runways'],runways['iata']))
        runways_count_df = pd.DataFrame(runways_count, columns = ['iata', 'runways'])
        runways_length_df = pd.DataFrame(runways_length, columns = ['iata', 'total_runway_length'])
        self._runways_stats_df = pd.merge(runways_count_df, runways_length_df, on = 'iata')

    def validate_runways(self, airport_runways: list[RunwayDict]) -> None:
        if airport_runways and any(runway['length_in_ft'] < 0 for runway in airport_runways):
            raise ValueError('Runway length cannot be negative')

    def count_runways(self, airport_runways: list[RunwayDict], iata: str) -> list[ str | int | None]:
        self.validate_runways(airport_runways)
        return [iata, len(airport_runways)]

    def sum_runways_len(self, airport_runways: list[RunwayDict], iata: str) -> list[ str | int | None]:
        self.validate_runways(airport_runways)
        return [iata, sum(runway['length_in_ft'] for runway in airport_runways)]

    @property
    def runways_stats_df(self) -> pd.DataFrame:
        return self._runways_stats_df
