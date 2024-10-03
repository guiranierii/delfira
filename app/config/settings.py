import os
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    dremio_user: str = os.getenv('DREMIO_USER')
    dremio_password: str = os.getenv('DREMIO_PASSWORD')
    dremio_login_endpoint: str = os.getenv('DREMIO_LOGIN_ENDPONT')
    dremio_arrow_endpoint: str = os.getenv('DREMIO_ARROW_ENDPOINT')
    loki_url: str = os.getenv('LOKI_URL')

    class Config:
        env_file = Path("/home/lakehouse/delfira/.env")

settings = Settings()
