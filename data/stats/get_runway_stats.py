from dataclasses import dataclass, field
from typing import Optional
import pandas as pd

@dataclass
class RunwayStats:
    runways: list[list[dict|None]] # type: ignore [index]
    count: list[int|None] = field(init=False)
    len: list[int|None] = field(init = False)

    def __post_init__(self) -> None:
        self.count = list(map(self.count_runways, self.runways))
        self.len = list(map(self.sum_runways_len, self.runways))

    def sum_runways_len(self, airport_runways: list) -> Optional[int]:
        if self.count is not None:
            total_runway_length = 0
            for i in airport_runways:
                temp_len = i["length_in_ft"]
                total_runway_length = total_runway_length + temp_len
                return total_runway_length
        return None

    def count_runways(self, airport_runways: list) -> Optional[int]:
        runway_counter: int|None
        runway_counter = len(airport_runways)
        if runway_counter == 0:
            runway_counter = None
        return runway_counter

    def runway_df(self) -> pd.DataFrame:
        runways_df = pd.DataFrame(self.count, columns=["runways_count"])
        runways_df["total_runway_length"] = self.len
        return runways_df
