""" Provides the API endpoint that makes a prediction on a target variable within a given set of data.
"""

import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Security
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from src.api.resources.airport import Airport
from src.api.resources.post_air_quality_response import PostAirQualityResponse
from src.utils.logging import setup_logger

# import logger
logger = setup_logger()

# import API key from environment variables
load_dotenv() # loads the variables from the .env file to the current session's environment
API_KEY = str(os.getenv('API_KEY'))
api_key_header = APIKeyHeader(name='X-API-key')

# API key authentication method
def get_api_key(api_key_attempt: str = Security(api_key_header)) -> str:
    if api_key_attempt == API_KEY:
        return api_key_attempt
    raise HTTPException(
        status_code=401,
        detail='Unauthorised: Invalid or missing API key',
    )

prediction_router = APIRouter(prefix='/air-quality')

@prediction_router.post('', response_model=PostAirQualityResponse, status_code=201)
async def predict_air_quality(airport: Airport, api_key: str = Security(get_api_key)) -> JSONResponse: # pylint: disable=unused-argument

    # Use airport input parameters to create air quality prediction and store as PostAirQualityResponse object
    air_quality_response = PostAirQualityResponse(air_quality=get_air_quality_prediction(airport))

    # Return a JSONResponse with the serialized dictionary
    return JSONResponse(content={'air_quality': air_quality_response.air_quality}, status_code=201)

def get_air_quality_prediction(airport: Airport) -> float:
    """ Accesses air quality prediction model.
    """
    logger.info('Input airport information: %s', airport)

    # TODO: Delaney process runway stats (e.g., number of runways, their lengths)

    return 2.12
