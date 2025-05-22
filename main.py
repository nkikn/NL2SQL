from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import sql

from backend.db.database import Base, engine
from backend.services.sample_data import insert_sample_data

app = FastAPI()

# CORS (for Streamlit communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(sql.router)

Base.metadata.create_all(bind=engine)

insert_sample_data()
