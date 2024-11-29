from fastapi import FastAPI

from app.settings import SETTINGS
from app.api.routers.default import router as default_router


app = FastAPI()
app.include_router(default_router)
