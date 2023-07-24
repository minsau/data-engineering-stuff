from pydantic_settings import BaseSettings
from pydantic import BaseModel

class Settings(BaseSettings):
    BQ_DATASET_PREFIX: str
    GOOGLE_CREDENTIALS_PATH: str
    GCP_SECRET_NAME: str
    BUCKET_NAME: str


settings = Settings()


class Secrets(BaseModel):
    HOME_LOCATION: str = None
    GOOGLE_MAPS_API_KEY: str = None


print(settings.GCP_SECRET_NAME)
secrets = Secrets(**settings.GCP_SECRET_NAME)