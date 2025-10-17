from apify_client import ApifyClient
from dotenv import dotenv_values

config = dotenv_values(".env")
api_token = config.get("APIFY_TOKEN")
if not api_token:
    raise ValueError("APIFY_TOKEN is missing from .env")

client = ApifyClient(api_token)

# Prepare the Actor input
run_input = {
    "hashtags": ["fyp"],
    "resultsPerPage": 100,
    "profileScrapeSections": ["videos"],
    "profileSorting": "latest",
    "excludePinnedPosts": False,
    "searchSection": "",
    "maxProfilesPerQuery": 10,
    "scrapeRelatedVideos": False,
    "shouldDownloadVideos": False,
    "shouldDownloadCovers": False,
    "shouldDownloadSubtitles": False,
    "shouldDownloadSlideshowImages": False,
    "shouldDownloadAvatars": False,
    "shouldDownloadMusicCovers": False,
    "proxyCountryCode": "None",
}

# Run the Actor and wait for it to finish
run = client.actor("GdWCkxBtKWOsKjdch").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)