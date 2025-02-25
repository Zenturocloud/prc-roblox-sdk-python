# Error Handling in the PRC SDK

This document explains how to handle errors when using the PRC SDK.

## Table of Contents

- [Error Classes](#error-classes)
- [Common Error Scenarios](#common-error-scenarios)
- [Error Codes](#error-codes)
- [Best Practices](#best-practices)
- [Advanced Error Handling](#advanced-error-handling)

## Error Classes

The PRC SDK provides several error classes to handle different types of errors:

### PrcError

Base exception for all PRC errors. All other error classes inherit from this.

### PrcApiError

Raised when the PRC API returns an error response.

**Properties:**
- `message`: The error message
- `status_code`: The HTTP status code (e.g., 400, 403, 500)
- `error_code`: The specific PRC error code (e.g., 2000, 3001)

Example:
```python
try:
    status = client.get_server_status()
except PrcApiError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
    print(f"Error Code: {e.error_code}")
```

### PrcConnectionError

Raised when there's a problem connecting to the PRC API. This could be due to network issues, DNS problems, etc.

**Properties:**
- `message`: The error message

Example:
```python
try:
    status = client.get_server_status()
except PrcConnectionError as e:
    print(f"Connection Error: {e.message}")
    print("Please check your internet connection.")
```

### PrcRateLimitError

Raised when you've hit a rate limit and the client is configured to raise exceptions on rate limits.

**Properties:**
- `message`: The error message
- `status_code`: Always 429
- `error_code`: Always 4001
- `retry_after`: The number of seconds to wait before retrying

Example:
```python
try:
    status = client.get_server_status()
except PrcRateLimitError as e:
    print(f"Rate Limited: {e.message}")
    print(f"Try again in {e.retry_after} seconds")
```

### PrcAuthenticationError

Raised when there's an authentication problem with your server key or API key.

**Properties:**
- `message`: The error message
- `status_code`: Always 403
- `error_code`: The specific authentication error code (e.g., 2000, 2001, 2002, 2003, 2004)

Example:
```python
try:
    status = client.get_server_status()
except PrcAuthenticationError as e:
    print(f"Authentication Error: {e.message}")
    print(f"Error Code: {e.error_code}")
    if e.error_code == 2002:
        print("Your server key is invalid or has expired.")
```

## Common Error Scenarios

### Authentication Errors

Authentication errors occur when there's a problem with your server key or API key.

```python
try:
    status = client.get_server_status()
except PrcAuthenticationError as e:
    if e.error_code == 2000:
        print("No server key provided")
    elif e.error_code == 2001:
        print("Incorrectly formatted server key")
    elif e.error_code == 2002:
        print("Invalid or expired server key")
    elif e.error_code == 2003:
        print("Invalid global API key")
    elif e.error_code == 2004:
        print("Server key is banned from API access")
    else:
        print(f"Authentication error: {e.message}")
```

### Rate Limit Errors

Rate limit errors occur when you've made too many requests in a short period of time.

```python
try:
    status = client.get_server_status()
except PrcRateLimitError as e:
    print(f"Rate limited. Try again in {e.retry_after} seconds")
    
    # Wait and retry
    import time
    time.sleep(e.retry_after)
    try:
        status = client.get_server_status()
    except PrcApiError as e:
        print(f"Error persists: {e.message}")
```

### Server-Related Errors

Server-related errors occur when there's a problem with the PRC server.

```python
try:
    response = client.execute_command(":h Hello World")
except PrcApiError as e:
    if e.error_code == 3002:
        print("The server is offline (has no players)")
    elif e.error_code == 4002:
        print("The command you're trying to run is restricted")
    elif e.error_code == 4003:
        print("The message you're trying to send is prohibited")
    else:
        print(f"API error: {e.message}")
```

### Connection Errors

Connection errors occur when there's a problem connecting to the PRC API.

```python
try:
    status = client.get_server_status()
except PrcConnectionError as e:
    print(f"Connection error: {e.message}")
    print("Please check your internet connection and try again")
```

## Error Codes

The PRC API uses the following error codes:

| Error Code | Description |
|------------|-------------|
| 0          | Unknown error |
| 1001       | Error communicating with Roblox / in-game private server |
| 1002       | Internal system error |
| 2000       | No server-key provided |
| 2001       | Incorrectly formatted server-key |
| 2002       | Invalid or expired server-key |
| 2003       | Invalid global API key |
| 2004       | Server-key banned from API access |
| 3001       | Invalid command in request body |
| 3002       | Server is offline (has no players) |
| 4001       | Rate limited |
| 4002       | Restricted command |
| 4003       | Prohibited message |
| 9998       | Restricted resource |
| 9999       | Out-of-date in-game server module |

## Best Practices

### Use a Try-Except Block for All API Calls

Always wrap API calls in a try-except block to handle potential errors gracefully:

```python
try:
    status = client.get_server_status()
    print(f"Server: {status.name}")
except PrcApiError as e:
    print(f"Error: {e.message}")
```

### Handle Specific Errors First

When catching exceptions, catch the most specific exceptions first:

```python
try:
    status = client.get_server_status()
except PrcAuthenticationError as e:
    print(f"Authentication error: {e.message}")
except PrcRateLimitError as e:
    print(f"Rate limited: {e.message}")
except PrcConnectionError as e:
    print(f"Connection error: {e.message}")
except PrcApiError as e:
    print(f"API error: {e.message}")
```

### Check Status Codes and Error Codes

Use status codes and error codes to determine the specific error:

```python
try:
    status = client.get_server_status()
except PrcApiError as e:
    if e.status_code == 400:
        print("Bad request")
    elif e.status_code == 403:
        print("Unauthorized")
    elif e.status_code == 404:
        print("Resource not found")
    elif e.status_code == 500:
        print("Server error")
    
    if e.error_code == 3002:
        print("Server is offline")
    elif e.error_code == 9999:
        print("Server module is out of date")
```

### Use Default Values

When handling errors, provide default values or fallbacks:

```python
try:
    players = client.get_players()
except PrcApiError:
    # Use an empty list as a fallback
    players = []

player_count = len(players)
print(f"Player count: {player_count}")
```

## Advanced Error Handling

### Retry with Exponential Backoff

For transient errors, implement exponential backoff:

```python
import time
import random

def get_server_status_with_retry(client, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.get_server_status()
        except PrcConnectionError as e:
            # Only retry on connection errors
            if attempt < max_retries - 1:
                # Exponential backoff with jitter
                sleep_time = (2 ** attempt) + random.random()
                print(f"Connection error: {e.message}. Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            else:
                # Last attempt failed
                raise
        except PrcApiError:
            # Don't retry on API errors
            raise

try:
    status = get_server_status_with_retry(client)
    print(f"Server: {status.name}")
except Exception as e:
    print(f"Failed after retries: {str(e)}")
```

### Logging Errors

Use the logging module to log errors:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prc-sdk")

try:
    status = client.get_server_status()
except PrcApiError as e:
    logger.error(f"API Error: {e.message} (Code: {e.error_code}, Status: {e.status_code})")
    # Handle error...
```

### Custom Error Handler

Create a custom error handler function:

```python
def handle_prc_error(error):
    if isinstance(error, PrcAuthenticationError):
        print(f"Authentication Error: {error.message}")
        print("Please check your server key")
        return False
    elif isinstance(error, PrcRateLimitError):
        print(f"Rate Limited: Try again in {error.retry_after} seconds")
        return False
    elif isinstance(error, PrcConnectionError):
        print(f"Connection Error: {error.message}")
        print("Please check your internet connection")
        return False
    elif isinstance(error, PrcApiError):
        print(f"API Error: {error.message}")
        print(f"Status: {error.status_code}, Code: {error.error_code}")
        return False
    else:
        print(f"Unexpected error: {str(error)}")
        return False

try:
    status = client.get_server_status()
    print(f"Server: {status.name}")
except Exception as e:
    if not handle_prc_error(e):
        # Additional error handling if needed
        pass
```
