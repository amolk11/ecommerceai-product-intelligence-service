from dotenv import load_dotenv

import os

load_dotenv()

HOST = os.getenv("HOST", "http://localhost:8000")
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found in environment variables.")
