from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SERVER_HOST: str
    SERVER_PORT: int
    RELOAD: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()