"""
Utility functions for the PRC SDK.
"""

import time
from datetime import datetime


def timestamp_to_datetime(timestamp):
    """
    Convert a Unix timestamp to a datetime object.
    
    Args:
        timestamp: The Unix timestamp (seconds since epoch).
        
    Returns:
        A datetime object representing the timestamp.
    """
    return datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(dt):
    """
    Convert a datetime object to a Unix timestamp.
    
    Args:
        dt: The datetime object.
        
    Returns:
        The Unix timestamp (seconds since epoch).
    """
    return int(dt.timestamp())


def extract_player_info(player_string):
    """
    Extract player name and ID from a player string.
    
    Args:
        player_string: A string in the format "PlayerName:Id".
        
    Returns:
        A dictionary containing the player name and ID.
    """
    parts = player_string.split(":")
    
    if len(parts) >= 2:
        return {
            "name": parts[0],
            "id": parts[1]
        }
    
    return {
        "name": parts[0] if parts else "",
        "id": ""
    }


def format_datetime(dt, format_string="%Y-%m-%d %H:%M:%S"):
    """
    Format a datetime object as a string.
    
    Args:
        dt: The datetime object.
        format_string: The format string to use.
        
    Returns:
        A formatted string representation of the datetime.
    """
    return dt.strftime(format_string)


def wait_for_rate_limit(retry_after, buffer=1):
    """
    Wait for a rate limit to expire.
    
    Args:
        retry_after: The number of seconds to wait.
        buffer: Additional buffer time to add (in seconds).
    """
    wait_time = max(1, retry_after + buffer)
    time.sleep(wait_time)


def parse_error_response(response_data):
    """
    Parse an error response from the API.
    
    Args:
        response_data: The JSON response data.
        
    Returns:
        A dictionary containing the error details.
    """
    return {
        "message": response_data.get("message", "Unknown error"),
        "error_code": response_data.get("code", 0),
        "retry_after": response_data.get("retry_after")
    }


def is_valid_server_key(server_key):
    """
    Check if a server key is valid (basic format check).
    
    Args:
        server_key: The server key to check.
        
    Returns:
        True if the server key appears to be valid, False otherwise.
    """
    return bool(server_key and isinstance(server_key, str) and len(server_key) > 8)


def make_rate_limit_info(headers):
    """
    Extract rate limit information from response headers.
    
    Args:
        headers: The response headers.
        
    Returns:
        A dictionary containing rate limit information.
    """
    return {
        "bucket": headers.get("X-RateLimit-Bucket", "unknown"),
        "limit": int(headers.get("X-RateLimit-Limit", 0)),
        "remaining": int(headers.get("X-RateLimit-Remaining", 0)),
        "reset": int(headers.get("X-RateLimit-Reset", 0)),
        "reset_at": timestamp_to_datetime(int(headers.get("X-RateLimit-Reset", 0)))
    }
