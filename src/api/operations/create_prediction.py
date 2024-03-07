""" Provides the API endpoint that makes a prediction on a target variable within a given set of data.
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Final

import pandas as pd
from fastapi import APIRouter, FastAPI, HTTPException, Security
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from src.api.resources.airport import Airport
from src.api.resources.post_air_quality_response import PostAirQualityResponse
from src.data.get_runway_stats import RunwayStats
from src.model.model import Model
from src.utils.logging import setup_logger

_logger = setup_logger()

API_KEY = os.getenv('API_KEY')
api_key_header = APIKeyHeader(name='X-API-key')

MODEL_PATH: Final[str] = './model/rf_model.pickle'

rf_model = None # type: ignore

def get_api_key(api_key_attempt: str = Security(api_key_header)) -> str:
    if api_key_attempt == API_KEY:
        return api_key_attempt
    raise HTTPException(status_code=401, detail='Unauthorised: Invalid or missing API key')

@asynccontextmanager
async def lifespan(app: FastAPI) ->  AsyncGenerator[None, None]:
    global rf_model
    rf_model = Model.load_trained_model(MODEL_PATH)
    yield


prediction_router = APIRouter(prefix='/air-quality')

@prediction_router.post('', response_model=PostAirQualityResponse, status_code=201)
async def predict_air_quality(airport: Airport,  api_key: str = Security(get_api_key)) -> JSONResponse:  # pylint: disable=unused-argument
    air_quality_response = PostAirQualityResponse(air_quality=get_air_quality_prediction(airport))
    return JSONResponse(content={'air_quality': air_quality_response.air_quality}, status_code=201)


def get_air_quality_prediction(airport: Airport) -> float:
    """ Accesses air quality prediction model.
    """
    _logger.info('Input airport information: %s', airport)
    # Preprocessing input data
    airports_df = pd.json_normalize(airport.model_dump())
    runways_input = pd.concat([airports_df[['runways']], airports_df['iata']], axis=1, join='outer')
    runways_stats_df = RunwayStats(runways_input).runways_stats_df
    input_df = pd.concat([airports_df.drop(['runways'], axis=1), runways_stats_df], axis=1)
    input_df = input_df[['altitude', 'runways', 'total_runway_length', 'total_arrivals', 'total_departures']]

    # Predict
    air_quality = rf_model.predict(input_df) # type: ignore[union-attr]
    return air_quality
