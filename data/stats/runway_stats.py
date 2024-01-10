from dataclasses import dataclass, field
import pandas as pd 

@dataclass 
class RunwayStats:
  runways: list
  count: list = field(init=False)
  len: list = field(init = False)

  def __post_init__(self) -> None:
    self.count = list(map(self.count_runways, self.runways))
    self.len = list(map(self.sum_runways_len, self.runways))
    return None
  
  def sum_runways_len(self, set: list) -> int:
    if self.count != None:
      total_runway_length = 0
      for i in set:
        temp_len = i["length_in_ft"]
        total_runway_length = total_runway_length + temp_len
      return total_runway_length
    else:
      return None

  def count_runways(self, set: list) -> int:
    count = len(set)
    if count == 0:
      count = None
    return count

  def runway_df(self) -> pd.DataFrame:
    runways_df = pd.DataFrame(self.count, columns=["runways_count"])
    runways_df["total_runway_length"] = self.len
    return runways_df

