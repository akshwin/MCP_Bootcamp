import urllib.request

def get_weather(location:str) -> str:
    """
    Get the weather for a given location
    
    Args:
        location: The location to get the weather for
        
    Returns:
        The weather for the given location
    """
    
    try:
        url = f"https://wttr.in/{location}?format=3"
        # Add a basic User-Agent to avoid occasional blocks from some environments.
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8').strip()
            return result
    except Exception as e:
        return f"Error getting weather: {e}"
    
    