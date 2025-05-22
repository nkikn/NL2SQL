# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import time
from sqlalchemy.exc import OperationalError


# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# for _ in range(10):
#     try:
#         engine = create_engine(DATABASE_URL)
#         conn = engine.connect()
#         conn.close()
#         break
#     except OperationalError:
#         print("Database not ready, retrying in 3 seconds...")
#         time.sleep(3)
# else:
#     raise Exception("Database connection failed after retries")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to use with FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
