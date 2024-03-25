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

        # Map lambda function to make a runway stats dict for each airport
        runways_stats = list(map(
            lambda iata, runways: {
                **({'iata': iata} if 'iata' in airports.columns else {}), #unpacks empty dict if iata DNE
                'runways_count': self.count_runways_at_airport(runways),
                'total_runway_length': self.sum_runways_len_at_airport(runways)
            },
            airports.get('iata', [None]), #provides an iterable in the case iata DNE
            airports['runways']
        ))

        self._runways_stats_df = pd.DataFrame(runways_stats)

    def validate_runways(self, single_airport_runways: list[RunwayDict]) -> None:
        if single_airport_runways and any(runway['length_in_ft'] < 0 for runway in single_airport_runways):
            raise ValueError('Runway length cannot be negative')

    def count_runways_at_airport(self, single_airport_runways: list[RunwayDict]) -> int | None:
        self.validate_runways(single_airport_runways)
        return len(single_airport_runways)

    def sum_runways_len_at_airport(self, single_airport_runways: list[RunwayDict]) -> int | None:
        self.validate_runways(single_airport_runways)
        return sum(runway['length_in_ft'] for runway in single_airport_runways)

    @property
    def runways_stats_df(self) -> pd.DataFrame:
        return self._runways_stats_df
