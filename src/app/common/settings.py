from pathlib import Path

from envparse import Env
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


env = Env()
env.read_envfile(".env")


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_SECONDS: int = env.int("ACCESS_TOKEN_EXPIRE_SECONDS")
    SECRET: str = env.str("SECRET")

    MAX_FILE_SIZE_MB: int = env.str("MAX_FILE_SIZE_MB")
    FILE_CHUNK_SIZE: int = env.str("FILE_CHUNK_SIZE", default=1024 * 1024 * 10)

    IMAGE_DIR_PATH: Path = Path(env.str("IMAGE_DIR_PATH"))
    CELERY_BROKER_URI: str = env.str("CELERY_BROKER_URI")
    CELERY_RESULT_BACKEND: str = env.str("CELERY_RESULT_BACKEND")
    SMTP_HOST: str = env.str("SMTP_HOST")
    SMTP_PORT: int = env.int("SMTP_PORT")
    SMTP_USER: str = env.str("SMTP_USER")
    SMTP_PASSWORD: str = env.str("SMTP_PASSWORD")
    DB_HOST: str = env.str("DB_HOST")
    DB_PORT: int = env.int("DB_PORT")
    DB_USER: str = env.str("DB_USER")
    DB_PASSWORD: str = env.str("DB_PASSWORD")
    DB_NAME: str = env.str("DB_NAME")
    ASYNC_DB_URI: str = str(
        PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            path=DB_NAME,
        )
    )


settings = Settings()
