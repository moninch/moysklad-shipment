from os import environ, getenv
from pydantic import BaseModel, SecretStr
from dotenv import load_dotenv

load_dotenv(".env")


class Settings(BaseModel):
    LOGGING_LEVEL: str

    TOKEN: str

    API_PORT: int
    API_HOST: str


SETTINGS = Settings(**environ)
