import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    model_config = SettingsConfigDict(
        env_file=os.getenv('ENV_FILE', '.env')
    )


settings = Settings()


def get_db_url():
    return (f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@'
            f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')
