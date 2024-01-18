"""
Aggregates all API routers and starts the API.
"""

import time
import uvicorn

from pydantic import BaseModel
from fastapi import FastAPI
from typing import List, Final

V1_URL_PREFIX: Final[str] = '/v1'

app = FastAPI(
    title='Air Quality Prediction Service',
    version='1.0.0',
    docs_url=None,
    redoc_url=None
)

# Pydantic class defintions
class Runway(BaseModel):
    length: float
    surface: str

class Airport(BaseModel):
    altitude: float
    runways: List[Runway]
    total_arrivals: int
    total_departures: int

class PostAirQualityResponse(BaseModel):
    air_quality: float

class ErrorItem(BaseModel):
    code: str
    message: str

class Error(BaseModel): 
    errors: List[ErrorItem]
    status_code: int

# Endpoint to predict air quality from airport information
@app.post("/air-quality", response_model=PostAirQualityResponse, status_code=201)
async def predict_air_quality(airport: Airport):
    # Replace the following line with the air quality prediction model
    predicted_air_quality = 2.12

    time.sleep(1)

    return {"air_quality": predicted_air_quality}

if __name__ == '__main__':
    uvicorn.run(app)