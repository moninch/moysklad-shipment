from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.routers import main_router_v1

from app.settings import SETTINGS

from app.api.routers.default import router as default_router


app = FastAPI()
app.include_router(default_router)
