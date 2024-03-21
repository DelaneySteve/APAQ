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
    airports: InitVar[pd.DataFrame]
    _runways_stats_df: pd.DataFrame = field(init=False)

    def __post_init__(self, airports: pd.DataFrame) -> None:

        # pass the runways list for each airport through the runways count and length functions
        runways_count = list(map(self.count_runways_at_airport, airports['runways'], airports['iata']))
        runways_length = list(map(self.sum_runways_len_at_airport, airports['runways'],airports['iata']))

        # put list into dataframe and label columns
        runways_count_df = pd.DataFrame(runways_count, columns = ['iata', 'runways_count'])
        runways_length_df = pd.DataFrame(runways_length, columns = ['iata', 'total_runway_length'])

        # merge columns based on matching iata
        self._runways_stats_df = pd.merge(runways_count_df, runways_length_df, on = 'iata')

    def validate_runways(self, single_airport_runways: list[RunwayDict]) -> None:
        if single_airport_runways and any(runway['length_in_ft'] < 0 for runway in single_airport_runways):
            raise ValueError('Runway length cannot be negative')

    def count_runways_at_airport(self, single_airport_runways: list[RunwayDict], iata: str) -> list[ str | int | None]:
        self.validate_runways(single_airport_runways)
        return [iata, len(single_airport_runways)]

    def sum_runways_len_at_airport(self, single_airport_runways: list[RunwayDict], iata: str) -> list[ str | int | None]:
        self.validate_runways(single_airport_runways)
        return [iata, sum(runway['length_in_ft'] for runway in single_airport_runways)]

    @property
    def runways_stats_df(self) -> pd.DataFrame:
        return self._runways_stats_df
