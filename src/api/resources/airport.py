from pydantic import BaseModel

from src.api.resources.runway import Runway


class Airport(BaseModel):
    iata: str
    altitude: int
    runways: list[Runway]
    total_arrivals: int
    total_departures: int
