"""Instagram extraction utilities built on the Apify Transcriber actor."""

from typing import Any, Dict

from utils.apify_client_config import client as default_client


def extract_instagram_content(url: str, api_client=default_client) -> Dict[str, Any]:
    """Fetch an Instagram transcript using the Apify social video transcriber."""

    run_input = {"start_urls": url}

    try:
        run = api_client.actor("tictechid/anoxvanzi-transcriber").call(run_input=run_input)
        dataset = api_client.dataset(run["defaultDatasetId"])
    except Exception as exc:  # pragma: no cover - network failure path
        return {
            "platform": "instagram",
            "url": url,
            "status": "error",
            "error": f"Failed to start Instagram transcription: {exc}",
            "text": "",
        }

    for item in dataset.iterate_items():
        status = item.get("status", "unknown")
        transcript = item.get("transcript", "") or ""

        payload: Dict[str, Any] = {
            "platform": "instagram",
            "url": url,
            "status": status,
            "text": transcript or "",
            "detected_language": item.get("detected_language"),
            "duration_sec": item.get("durationSec"),
            "timestamp": item.get("timestamp"),
            "video_id": item.get("videoId"),
        }

        fallback_message = item.get("error") or item.get("transcript")
        if not transcript and isinstance(fallback_message, str) and fallback_message:
            payload["text"] = fallback_message

        if status != "success":
            payload["error"] = fallback_message or "Unknown transcription error"
        else:
            payload["transcript"] = transcript or fallback_message or ""

    return {
        "platform": "instagram",
        "url": url,
        "status": "error",
        "error": "No transcription data returned from Apify.",
        "text": "",
    }
