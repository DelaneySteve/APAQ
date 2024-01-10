from dataclasses import dataclass, field
import pandas as pd

@dataclass 
class FlightStats:
  flights: list
  flights_count_list: list = field(init = False)
  
  def __post_init__(self) -> None:
    self.flights_count_list = list(map(self.count_flights, self.flights))
    return None

  #total arrivals or departures 
  def count_flights(self, set: list) -> dict:
    total = len(set)
    departures = 0
    arrivals = 0 
    if total != 0:
      airport = set[0]["origin_iata"]
    
      for i in set:
        if i["origin_iata"] == airport:
          departures = departures + 1
        else:
          arrivals = arrivals + 1
    else:
      total = None 
      arrivals = None
      departures = None  
    flight_data = {"arrivals": arrivals, "departures": departures, "total": total}      
    return flight_data

  def flight_count_df(self):
    flight_count_df = pd.DataFrame(self.flights_count_list)
    return flight_count_df