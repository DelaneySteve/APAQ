""" Aggregates all API routers and starts the API.
"""

import os
import uvicorn

from fastapi import FastAPI, APIRouter
from typing import Final
from src.api.operations.create_prediction import prediction_router

# Allow versioning of the API via the URI path
BASE_PATH: Final[str] = "/v1"
app = FastAPI()
router = APIRouter()
router.prefix = BASE_PATH

# Add endpoints connected to other routers to this router.
app.include_router(router)
app.include_router(prediction_router)

# Run the API
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app=app, port=port)
