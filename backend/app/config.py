from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Default to SQLite for easy local development; override in Docker via env
    database_url: str = "sqlite:///./zquant.db"
    redis_url: str = "redis://redis:6379/0"
    tf_serving_url: str = "http://tfserving:8501/v1/models/zqt_model:predict"

    class Config:
        env_file = ".env"


settings = Settings()


