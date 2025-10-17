from apify_client_config import client as default_client


def extract_tiktok_content(url: str, api_client=default_client):
    """Fetch TikTok subtitles via the Apify TikTok Scraper actor."""
    run_input = {
        "videoUrls": [url],
        "resultsPerPage": 1,
        "shouldDownloadSubtitles": True,
        "shouldDownloadVideos": False,
        "proxyCountryCode": "None",
    }

    run = api_client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
    dataset = api_client.dataset(run["defaultDatasetId"])

    for item in dataset.iterate_items():
        subtitles = item.get("subtitles") or []
        return subtitles
    return None


if __name__ == "__main__":
    extract_tiktok_content("https://vt.tiktok.com/ZSDvURRjQ/")
