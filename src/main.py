""" Aggregates all API routers and starts the API.
"""

import os
from typing import Final

import uvicorn
from fastapi import APIRouter, FastAPI

from src.api.operations.create_prediction import lifespan, prediction_router

# Allow versioning of the API via the URI path
BASE_PATH: Final[str] = '/v1'
app = FastAPI(lifespan = lifespan)
router = APIRouter()
router.prefix = BASE_PATH

# Add endpoints connected to other routers to this router.
app.include_router(router)
app.include_router(prediction_router)

# Run the API
if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    uvicorn.run(app=app, port=port)
