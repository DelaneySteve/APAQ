from dataclasses import dataclass
from typing import Any


@dataclass(unsafe_hash=True)
class Flight:
    aircraft_model: str | None
    airline: str | None
    destination_iata: str | None
    destination_icao: str | None
    flight_number: str
    long_aircraft_name: str | None
    origin_iata: str | None
    origin_icao: str | None
    scheduled_arrival: int
    scheduled_departure: int

    @classmethod
    def new_flight(cls, airport_iata: str | None, airport_icao: str | None, /, *, flight_data: dict[str, Any],
                   is_arrival: bool) -> 'Flight':
        flight_info = flight_data['flight']
        if is_arrival:
            origin_info = flight_info['airport']['origin']
            origin_iata = None if not origin_info else origin_info['code']['iata']
            origin_icao = None if not origin_info else origin_info['code']['icao']
            destination_iata = airport_iata
            destination_icao = airport_icao
        else:
            destination_info = flight_info['airport']['destination']
            destination_iata = None if not destination_info else destination_info['code']['iata']
            destination_icao = None if not destination_info else destination_info['code']['icao']
            origin_iata = airport_iata
            origin_icao = airport_icao

        airline = None if not flight_info['airline'] else flight_info['airline']['name']
        aircraft_model = None if not flight_info['aircraft'] else flight_info['aircraft']['model']['code']
        aircraft_long_name = None if not flight_info['aircraft'] else flight_info['aircraft']['model']['text']
        return Flight(
            aircraft_model=aircraft_model,
            airline=airline,
            destination_iata=destination_iata,
            destination_icao=destination_icao,
            flight_number=flight_info['identification']['number']['default'],
            long_aircraft_name=aircraft_long_name,
            origin_iata=origin_iata,
            origin_icao=origin_icao,
            scheduled_arrival=flight_info['time']['scheduled']['arrival'],
            scheduled_departure=flight_info['time']['scheduled']['departure']
        )

    def json(self) -> dict[str, str | int]:
        return self.__dict__

    def csv(self) -> tuple[list[str], list[str | int]]:
        return list(self.__dict__.keys()), list(self.__dict__.values())
