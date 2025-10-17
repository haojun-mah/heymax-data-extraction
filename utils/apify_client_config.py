import os
from pathlib import Path

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("APIFY_TOKEN"):
    project_root = Path(__file__).resolve().parents[1]
    load_dotenv(project_root / ".venv/.env")

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
if not APIFY_TOKEN:
    raise ValueError("APIFY_TOKEN is missing from environment variables")

client = ApifyClient(APIFY_TOKEN)
