import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLAL_DATABASE_URL = f"postgresql://{os.getenv('db_user')}:{os.getenv('db_password')}@{os.getenv('db_host')}/{os.getenv('db_name')}"
engine = create_engine(SQLAL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()