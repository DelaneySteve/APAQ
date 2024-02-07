from pydantic import BaseModel

from src.api.resources.runway import Runway
class Airport(BaseModel):
    altitude: int
    runways: list[Runway]
    total_arrivals: int
    total_departures: int

    def to_json(self) -> dict[str, str | int | list[dict[str, int]]]:
        return {
            'altitude': self.altitude,
            'runways': [runway.to_json() for runway in self.runways],
            'total_arrivals': self.total_arrivals,
            'total_departures': self.total_departures
            }
    