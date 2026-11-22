from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlite_db_name = 'mydb.db'