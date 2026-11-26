from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setting import Settings


settings = Settings()

engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(bind=engine)