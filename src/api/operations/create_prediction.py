import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import pandas as pd
from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from src.api.errors import UnauthorizedError, new_error_response
from src.api.resources.airport import Airport
from src.api.resources.post_air_quality_response import PostAirQualityResponse
from src.data.get_runway_stats import RunwayStats
from src.model.model import Model
from src.utils.logging import setup_logger

_logger = setup_logger()
rf_model = None  # type: ignore
prediction_router = APIRouter(prefix='/air-quality')

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # pylint: disable=unused-argument
    global rf_model
    rf_model = Model.load_trained_model()
    yield


@prediction_router.post('', response_model=PostAirQualityResponse, status_code=201)
async def predict_air_quality(airport: Airport, api_key: str = Depends(APIKeyHeader(name='X-API-key'))) -> PostAirQualityResponse | JSONResponse:  # pylint: disable=line-too-long
    if api_key != os.getenv('API_KEY'):
        return JSONResponse(
            content=new_error_response([UnauthorizedError()], status=UnauthorizedError.status_code),
            status_code=UnauthorizedError.status_code
        )
    return PostAirQualityResponse(air_quality=_get_air_quality_prediction(airport))


def _get_air_quality_prediction(airport: Airport) -> float:
    _logger.info('Input airport information: %s', airport)
    # Preprocessing input data
    airports_df = pd.json_normalize(airport.model_dump())
    runways_stats_df = RunwayStats(airports_df).runways_stats_df
    input_df = pd.concat([airports_df.drop(['runways'], axis=1), runways_stats_df], axis=1)
    input_df = input_df[['altitude', 'runways_count', 'total_runway_length', 'total_arrivals', 'total_departures']]

    # Predict
    air_quality = rf_model.predict(input_df)  # type: ignore[union-attr]
    return air_quality
