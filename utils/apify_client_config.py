import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
if not APIFY_TOKEN:
    raise ValueError("APIFY_TOKEN is missing from environment variables")

client = ApifyClient(APIFY_TOKEN)
