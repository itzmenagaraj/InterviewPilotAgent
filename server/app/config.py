import os
from dotenv import load_dotenv

load_dotenv()

AGENT_BASE_URL = os.getenv("AGENT_BASE_URL", "http://localhost:5001").rstrip("/")
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:8000").split(",")
    if origin.strip()
]
