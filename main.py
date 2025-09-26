"""
Main orchestrator script for URL content extraction workflow
This script takes a URL, classifies it, and calls the appropriate extractor
"""

import sys
from link_classifier import classify_link
from youtube_extracter import extract_youtube_content
from instagram_extractor import extract_instagram_content
from tiktok_extractor import extract_tiktok_content

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
    else:
        print(f"Unknown platform: {platform}")
        result = {
            "platform": "unknown",
            "url": url,
            "status": "error",
            "message": f"Unsupported platform: {platform}"
        }
    
    print("Processing complete!")
    print("=" * 60)
    
    return result

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
