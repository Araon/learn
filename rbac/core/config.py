from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    model_config = {'env_file': ".env"}

settings = Settings()
