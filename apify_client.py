from apify_client import ApifyClient
from dotenv import load_dotenv
import os

load_dotenv()
client = ApifyClient(os.environ["APIFY_TOKEN"])
