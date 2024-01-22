"""
Provides the API endpoint that makes a prediction on a target variable within a given set of data.
"""

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from api.resources.airport import Airport
from api.resources.post_air_quality_response import PostAirQualityResponse

prediction_router = APIRouter(prefix="/air-quality")

@prediction_router.post("", response_model=PostAirQualityResponse, status_code=201)
async def predict_air_quality(airport: Airport):

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
