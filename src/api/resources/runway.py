from pydantic import BaseModel

class Runway(BaseModel):
    length: float
    surface: str