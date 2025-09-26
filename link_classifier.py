import re

def classify_link(url):
    """
    Classify a URL to determine if it's from YouTube, Instagram, or TikTok
    
    Args:
        url (str): The URL to classify
        
    Returns:
        str: The platform name ('youtube', 'instagram', 'tiktok') or 'unknown'
    """
    
    # YouTube patterns
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)',
        r'(?:https?://)?(?:www\.)?(?:m\.youtube\.com/watch\?v=)',
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/shorts/)'
    ]
    
    # Instagram patterns
    instagram_patterns = [
        r'(?:https?://)?(?:www\.)?instagram\.com/p/',
        r'(?:https?://)?(?:www\.)?instagram\.com/reel/',
        r'(?:https?://)?(?:www\.)?instagram\.com/tv/',
        r'(?:https?://)?(?:www\.)?instagram\.com/stories/',
        r'(?:https?://)?(?:www\.)?instagr\.am/p/'
    ]
    
    # TikTok patterns
    tiktok_patterns = [
        r'(?:https?://)?(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+',
        r'(?:https?://)?(?:vm\.)?tiktok\.com/[\w.-]+',
        r'(?:https?://)?(?:www\.)?tiktok\.com/t/[\w.-]+',
        r'(?:https?://)?(?:www\.)?tiktok\.com/v/\d+'
    ]
    
    # Check for YouTube
    for pattern in youtube_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return 'youtube'
    
    # Check for Instagram
    for pattern in instagram_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return 'instagram'
    
    # Check for TikTok
    for pattern in tiktok_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return 'tiktok'
    
    return 'unknown'
