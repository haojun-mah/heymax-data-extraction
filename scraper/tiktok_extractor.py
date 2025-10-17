import requests

from utils.apify_client_config import client as default_client

# As extracter returns vtt subtitle file
def _parse_vtt(vtt_text: str) -> str:
    """Convert VTT subtitle content into a plain text transcript."""
    lines = []
    for raw_line in vtt_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("WEBVTT") or "-->" in line:
            continue
        lines.append(line)
    return " ".join(lines)


def extract_tiktok_content(url: str, api_client=default_client):
    """Fetch TikTok subtitles via the Apify TikTok Scraper actor."""
    run_input = {
        "postURLs": [url],
        "resultsPerPage": 1,
        "shouldDownloadSubtitles": True,
        "shouldDownloadVideos": False,
        "proxyCountryCode": "None",
    }

    run = api_client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
    dataset = api_client.dataset(run["defaultDatasetId"])

    for item in dataset.iterate_items():
        subtitles = item.get("subtitles") or []
        transcript = " ".join(
            snippet.get("text", "").strip() for snippet in subtitles if snippet.get("text")
        )
        transcript_source = "inline"

        if not transcript:
            subtitle_links = item.get("videoMeta", {}).get("subtitleLinks") or []
            download_link = subtitle_links[0].get("downloadLink") if subtitle_links else None
            if download_link:
                response = requests.get(download_link, timeout=15)
                response.raise_for_status()
                transcript = _parse_vtt(response.text)
                transcript_source = "vtt"

        payload = {
            "platform": "tiktok",
            "url": url,
            "text": transcript,
            "transcript_source": transcript_source,
            "metadata": {
                "id": item.get("id"),
                "author": item.get("authorMeta", {}).get("name"),
                "createTime": item.get("createTimeISO"),
                "music": item.get("musicMeta", {}).get("musicName"),
            },
            "status": "success",
        }
        return payload
    return {
        "platform": "tiktok",
        "url": url,
        "text": "",
        "transcript_source": "none",
        "status": "no_transcript",
    }
