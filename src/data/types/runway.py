from dataclasses import dataclass
from typing import Any


@dataclass(unsafe_hash=True)
class Runway:
    name: str
    length_in_m: int
    length_in_ft: int
    surface: str

    @classmethod
    def new_runway(cls, runway_info: dict[str, Any]) -> 'Runway':
        return Runway(
            name=runway_info['name'],
            length_in_m=runway_info['length']['m'],
            length_in_ft=runway_info['length']['ft'],
            surface=runway_info['surface']['name']
        )

    def json(self) -> dict[str, str | int]:
        return self.__dict__
