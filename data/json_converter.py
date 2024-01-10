from dataclasses import dataclass, field

import pandas as pd
import json

@dataclass
class DataConverter:
  raw_data: dict 
  airports_df: pd.DataFrame = field(init = False)
  runways: list = field(init = False)
  flights: list = field(init = False)
  
  def __post_init__(self) -> None:
    self.airports_df = pd.DataFrame(self.raw_data["airports"])
    self.flights = self.airports_df.pop("flights").to_list()
    self.runways = self.airports_df.pop("runways").to_list()
    return None
  
  def save_runways(self) -> None:
    with open("/runways.json", "w",encoding="utf-8") as f:
      json.dump(self.runways, f)
    return None
  
  def save_flights(self) -> None:
    with open("/runways.json", "w",encoding="utf-8") as f:
      json.dump(self.flights, f)
    return None
  
  def save_airports_to_csv(self) -> None:
    self.airports_df.to_csv("/airports.csv", sep=",", index=False, encoding="utf-8")
    return None