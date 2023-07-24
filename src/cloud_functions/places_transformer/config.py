from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from google.cloud import secretmanager
import json

class Settings(BaseSettings):
    BQ_DATASET_PREFIX: str
    GOOGLE_CREDENTIALS_PATH: str
    GCP_SECRET_VALUE: Optional[str] = None
    GCP_SECRET_NAME: str
    BUCKET_NAME: str
    PROJECT_ID: str
    ENVIRONMENT: str = 'prod'

settings = Settings()


class Secrets(BaseModel):
    HOME_LOCATION: str
    GOOGLE_MAPS_API_KEY: str

def get_app_secrets() -> Secrets:
    if settings.ENVIRONMENT == 'dev':
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{settings.PROJECT_ID}/secrets/{settings.GCP_SECRET_NAME}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        data_str = response.payload.data.decode("UTF-8")
    else:
        data_str = settings.GCP_SECRET_NAME
    
    return Secrets(**json.loads(data_str))