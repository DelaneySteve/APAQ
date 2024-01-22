from pydantic import BaseModel
from typing import List

from api.resources.runway import Runway

class Airport(BaseModel):
    altitude: float
    runways: List[Runway]
    total_arrivals: int
    total_departures: int