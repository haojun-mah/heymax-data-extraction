"""Main orchestrator for URL content extraction workflow."""

import json
import sys
from datetime import datetime
from pathlib import Path

from utils.link_classifier import classify_link
from scraper.youtube_extracter import extract_youtube_content
from scraper.instagram_extractor import extract_instagram_content
from scraper.tiktok_extractor import extract_tiktok_content

def process_url(url):
    """
    Main orchestrator function that processes a URL through the complete workflow
    
    Args:
        url (str): The URL to process
        
    Returns:
        dict: Extracted content data
    """
    
    # Step 1: Classify the URL
    print("-" * 40)
    print("Classifying URL...")
    platform = classify_link(url)
    
    # Step 2: Route to appropriate extractor based on classification
    if platform == 'youtube':
        print("Calling YouTube extractor...")
        result = extract_youtube_content(url)
    elif platform == 'instagram':
        print("Calling Instagram extractor...")
        result = extract_instagram_content(url)
    elif platform == 'tiktok':
        print("Calling TikTok extractor...")
        result = extract_tiktok_content(url)
    elif platform == 'airbnb':
        print("airbnb links are not supported for extraction.")
        result = {
            "platform": "airbnb",
            "url": url,
            "status": "skipped",
            "message": "airbnb links are not supported for content extraction"
        }
    else:
        print(f"Unknown platform: {platform}")
        result = {
            "platform": "unknown",
            "url": url,
            "status": "error",
            "message": f"Unsupported platform: {platform}"
        }
    
    save_result(result, platform, url)

    print("Processing complete!")
    print("=" * 60)

    return result


def save_result(result, platform, url):
    """Persist the extraction result to <platform>.json."""

    output_platform = (platform or result.get("platform") or "unknown").lower()
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M")
    filename = f"{output_platform}-{timestamp}.json"
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / filename
    payload_for_file = result
    if isinstance(result, dict):
        payload_for_file = {**result}
        if output_platform == "youtube" and "text" in payload_for_file:
            payload_for_file = {"text": payload_for_file["text"]}
            json_str = json.dumps(payload_for_file, ensure_ascii=False)
        else:
            if "platform" not in payload_for_file:
                payload_for_file["platform"] = output_platform
            if "url" not in payload_for_file:
                payload_for_file["url"] = url
            json_str = json.dumps(payload_for_file, indent=2, ensure_ascii=False)
    else:
        json_str = json.dumps(result, indent=2, ensure_ascii=False)

    output_path.write_text(json_str)
    print(f"Saved output to {output_path}")

def main():
    """
    Main function to handle command line arguments or interactive input
    """
    
    # Takes in URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Please enter the URL to process: ").strip()
        
        if not url:
            print("No URL provided. Exiting.")
            return
    
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        print("Warning: URL doesn't start with http:// or https://")
        print("Attempting to process anyway...")
    
    # Process the URL with
    try:
        result = process_url(url)
        
        
        if 'error' in result:
            print(f"Error: {result['error']}")
        elif 'message' in result:
            print(f"Message: {result['message']}")
        else:
            print(f"URL: {result.get('url', 'N/A')}")
            print(f"Platform: {result.get('platform', 'N/A')}")
            print(f"Status: {result.get('status', 'success')}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError in orchestrator: {e}")
        print("Please check your URL and try again.")

if __name__ == "__main__":
    main()
