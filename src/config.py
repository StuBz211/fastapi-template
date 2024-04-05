from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # common settings
    SECRET_KEY: str = "SECRET_KEY"
    PYTHONPATH: str = "src"
    API_BASE_DOMAIN: str

    MAIL_HOST: str = "mailhog"
    MAIL_PORT: int = 1025
    MAIL_LOGIN: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_FROM: str = 'template@fastapi.ru'

    # infa settings
    DATABASE_URL: str
    BROKER_URL: str

    # auth settings
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 24 * 60

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str

    class Config:
        env_file = ["dev.env", ".env"]


settings = Settings()
