# Rate Limits in the PRC API

This document explains how rate limits work in the PRC API and how the PRC SDK handles them.

## Table of Contents

- [Understanding PRC API Rate Limits](#understanding-prc-api-rate-limits)
- [Rate Limit Headers](#rate-limit-headers)
- [SDK Rate Limit Handling](#sdk-rate-limit-handling)
- [Configuring Rate Limit Behavior](#configuring-rate-limit-behavior)
- [Best Practices](#best-practices)

## Understanding PRC API Rate Limits

The PRC API enforces rate limits to prevent abuse and ensure fair usage. Rate limits apply per global API key, and when not provided, per IP address.

There are two types of rate limits:

1. **Global Rate Limit**: Applies to all API requests.
2. **Per-Route Rate Limit**: Applies to specific routes that are more intensive or subject to abuse.

For example, the `POST` route to send a command to a PRC server has a stricter limit (typically 1 request per 5 seconds) compared to other routes.

## Rate Limit Headers

The PRC API includes rate limit information in the response headers:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Bucket` | The rate limit bucket (e.g., "global" or "command-[Server-Key]") |
| `X-RateLimit-Limit` | The maximum number of requests allowed in the current time window |
| `X-RateLimit-Remaining` | The number of requests remaining in the current time window |
| `X-RateLimit-Reset` | Unix timestamp when the rate limit resets |

When a rate limit is exceeded, the API responds with a `429 Too Many Requests` status code and includes:

- A message explaining the rate limit
- The time to wait before retrying (`retry_after`) in seconds
- The rate limit bucket that was hit

## SDK Rate Limit Handling

The PRC SDK provides three different ways to handle rate limits:

### 1. Wait and Retry (Default)

```python
from src import PrcClient, RateLimitBehavior

client = PrcClient(
    server_key="your-server-key",
    rate_limit_behavior=RateLimitBehavior.WAIT_AND_RETRY
)
```

With this behavior:
- When a rate limit is hit, the SDK automatically waits for the specified time
- After waiting, it retries the request automatically
- If the rate limit persists after multiple retries, it raises a `PrcRateLimitError`

This is the most convenient option as it handles rate limits transparently.

### 2. Raise Exception

```python
from src import PrcClient, RateLimitBehavior

client = PrcClient(
    server_key="your-server-key",
    rate_limit_behavior=RateLimitBehavior.RAISE_EXCEPTION
)
```

With this behavior:
- When a rate limit is hit, the SDK immediately raises a `PrcRateLimitError`
- The exception includes a `retry_after` property indicating how long to wait
- Your code must catch the exception and handle the rate limit manually

Example:

```python
try:
    status = client.get_server_status()
except PrcRateLimitError as e:
    print(f"Rate limited! Try again in {e.retry_after} seconds")
    # Wait and retry manually
    import time
    time.sleep(e.retry_after)
    status = client.get_server_status()
```

### 3. Return Error

```python
from src import PrcClient, RateLimitBehavior

client = PrcClient(
    server_key="your-server-key",
    rate_limit_behavior=RateLimitBehavior.RETURN_ERROR
)
```

With this behavior:
- When a rate limit is hit, the SDK returns a dictionary with error information
- The dictionary includes keys for `error`, `message`, `status_code`, `error_code`, and `retry_after`
- Your code must check if the response is a dictionary with an `error` key

Example:

```python
response = client.get_server_status()
if isinstance(response, dict) and response.get("error"):
    print(f"Error: {response.get('message')}")
    if response.get("status_code") == 429:
        print(f"Rate limited! Try again in {response.get('retry_after')} seconds")
else:
    print(f"Server Name: {response.name}")
```

## Configuring Rate Limit Behavior

You can configure rate limit behavior when creating the client:

```python
from src import PrcClient, RateLimitBehavior

client = PrcClient(
    server_key="your-server-key",
    rate_limit_behavior=RateLimitBehavior.WAIT_AND_RETRY  # Default
)
```

## Best Practices

To avoid hitting rate limits:

1. **Don't Poll Excessively**: Avoid making frequent repeated requests to the same endpoint. For example, don't poll server status every second.

2. **Implement Backoff Strategies**: When you hit a rate limit, increase your wait time before retrying. The SDK does this automatically in `WAIT_AND_RETRY` mode.

3. **Use a Global API Key**: If you need higher rate limits, use a global API key.

4. **Cache Responses**: Cache responses where appropriate to reduce the number of API calls.

5. **Respect Rate Limit Headers**: The SDK automatically extracts rate limit information from response headers. You can access this information via `client.rate_limit_info`:

```python
status = client.get_server_status()
rate_info = client.rate_limit_info
print(f"Remaining requests: {rate_info['remaining']}/{rate_info['limit']}")
print(f"Reset at: {rate_info['reset_at'].strftime('%Y-%m-%d %H:%M:%S')}")
```

6. **Handle Rate Limits Gracefully**: Ensure your application handles rate limits appropriately. The default `WAIT_AND_RETRY` behavior is recommended for most cases.

## Rate Limit Error Codes

When a rate limit is exceeded, the API returns an error code of `4001`. The PRC SDK raises a `PrcRateLimitError` with this error code.

## Repeat Offender Policy

The PRC API may apply stricter rate limits to clients that repeatedly ignore rate limits. Always respect the `retry_after` values and rate limit headers.
