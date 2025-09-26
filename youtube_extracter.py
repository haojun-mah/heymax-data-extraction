import re
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

def extract_youtube_content(url):
    """
    Extract transcript content from YouTube URL
    
    Args:
        url (str): YouTube URL
        
    Returns:
        dict: Extracted transcript data
    """
    print(f"Processing YouTube URL: {url}")
    
    try:
        # Extract Video ID from URL as this API takes in Video ID 
        video_id_match = re.search(r'(?:v=|youtu\.be/|embed/|v/|shorts/)([^&\n?#]+)', url)
        if not video_id_match:
            raise ValueError("Could not extract video ID from URL")
        
        video_id = video_id_match.group(1)
        print(f"Extracted video ID: {video_id}")

        # Init api and fetch transcript
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)

        raw_data = fetched_transcript.to_raw_data()

        # Create a simple JSON with text, timestamp and metadata
        transcript_json = {
            "platform": "youtube",
            "url": url,
            "video_id": fetched_transcript.video_id,
            "language": fetched_transcript.language,
            "language_code": fetched_transcript.language_code,
            "is_generated": fetched_transcript.is_generated,
            "transcript": []
        }

        # Create a simple JSON with only text content
        text_segments = []

        for snippet in raw_data:
            transcript_json["transcript"].append({
                "text": snippet["text"],
                "start_time": snippet["start"],
                "duration": snippet["duration"],
                "end_time": snippet["start"] + snippet["duration"]
            })
            text_segments.append(snippet["text"])

        combined_text = " ".join(text_segments)
        text_only_json = {"text": combined_text}

        # Save both versions
        with open('youtube_transcript.json', 'w', encoding='utf-8') as f: 
            json.dump(transcript_json, f, indent=2, ensure_ascii=False)
            
        with open('youtube_text_only.json', 'w', encoding='utf-8') as f: 
            json.dump(text_only_json, f, indent=2, ensure_ascii=False)
        
        print("YouTube content saved to youtube_transcript.json and youtube_text_only.json")
        return transcript_json
        
    except Exception as e:
        error_data = {
            "platform": "youtube",
            "url": url,
            "status": "error",
            "error": str(e)
        }
        print(f"Error extracting YouTube content: {e}")
        return error_data
