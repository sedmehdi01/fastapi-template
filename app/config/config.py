from pydantic import BaseSettings
from dotenv import load_dotenv


load_dotenv(verbose=True)


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ALLOWED_HOSTS: str
    DEBUG: bool = True

    # databases
    MONGODB_URI: str
    MONGODB_DB_NAME: str
    REDIS_URI: str

    # Email credential
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    HOST: str
    PORT: int

    class Config:
        env_file = ".env"


settings = Settings()
