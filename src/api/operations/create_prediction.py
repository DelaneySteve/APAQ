"""
Provides the API endpoint that makes a prediction on a target variable within a given set of data.
"""

from fastapi import APIRouter, HTTPException
from api.resources.airport import Airport
from api.resources.post_air_quality_response import PostAirQualityResponse

prediction_router = APIRouter(prefix="/air-quality")

@prediction_router.post("", response_model=PostAirQualityResponse, status_code=201)
async def predict_air_quality(airport: Airport):

# Temporary check that airport data has been received
    print("Received airport information:", airport.dict())

    # Replace this with your actual air quality prediction result
    predicted_air_quality = 2.12

    return {"air_quality": predicted_air_quality}
