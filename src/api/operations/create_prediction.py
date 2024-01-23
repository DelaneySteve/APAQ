"""
Provides the API endpoint that makes a prediction on a target variable within a given set of data.
"""

import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.resources.airport import Airport
from api.resources.post_air_quality_response import PostAirQualityResponse

# import API key from environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="create-prediction-API-key")

# API key authentication method
def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=401,
        detail="Unauthorised: Invalid or missing API key",
    )

prediction_router = APIRouter(prefix="/air-quality")

@prediction_router.post("", response_model=PostAirQualityResponse, status_code=201)
async def predict_air_quality(airport: Airport, api_key: str = Security(get_api_key)):

    # Use airport input parameters to create air quality prediction and store as PostAirQualityResponse object
    air_quality_response = PostAirQualityResponse(air_quality=get_air_quality_prediction(airport))

    # Convert the object to a dictionary to allow it to be JSONified
    response_dict = jsonable_encoder(air_quality_response)

    # Return a JSONResponse with the serialized dictionary
    return JSONResponse(content=response_dict, status_code=201)

def get_air_quality_prediction(airport: Airport):
    """
    Accesses air quality prediction model.

    Returns float
    """

    return 2.12
