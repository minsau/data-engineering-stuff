from pydantic import BaseSettings

class Settings(BaseSettings):
    GOOGLE_MAPS_API_KEY: str
    BQ_DATASET_PREFIX: str
    GOOGLE_CREDENTIALS_PATH: str
    HOME_LOCATION: str

    class Config:
        env_file = ".env"

settings = Settings()