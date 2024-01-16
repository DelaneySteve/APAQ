from dataclasses import dataclass, field
from typing import List
import json
import pandas as pd
from src.data.types import Airport
from typing import Any


@dataclass
class DataConverter:
    raw_data: dict[str, list[Airport]]
    airports_df: pd.DataFrame = field(init = False)
    runways: pd.DataFrame = field(init = False)
    flights: pd.DataFrame = field(init = False)

    def __post_init__(self) -> None:
        self.airports_df = pd.DataFrame(self.raw_data["airports"])
        self.flights = self.airports_df[["flights"]]
        self.runways = self.airports_df[["runways"]]
        self.airports_df = self.airports_df.drop(["flights","runways"],axis = 1)

    def save_runways(self) -> None:
        with open("/runways.json", "w",encoding="utf-8") as f:
            json.dump(self.runways, f)

    def save_flights(self) -> None:
        with open("/runways.json", "w",encoding="utf-8") as f:
            json.dump(self.flights, f)

    def save_airports_to_csv(self) -> None:
        self.airports_df.to_csv("/airports.csv", sep=",", index=False, encoding="utf-8")
