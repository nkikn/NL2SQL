from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import sql

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
