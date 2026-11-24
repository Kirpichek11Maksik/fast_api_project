from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5433
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_NAME: str = 'zxcdb'
    CACHE_HOST: str = '127.0.0.1'
    CACHE_PORT: str = '6379'
    CACHE_DB: int = 0