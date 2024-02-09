from pydantic import BaseModel


class PostAirQualityResponse(BaseModel):
    air_quality: float
