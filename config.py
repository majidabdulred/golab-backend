from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TESTING: bool = False
    BASE_METEX_API_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    DB_SRV: str
    EMAIL_PASSWORD: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
