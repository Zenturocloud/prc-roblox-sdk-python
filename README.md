# PRC API SDK for Python

![PRC API](https://img.shields.io/badge/PRC-API_SDK-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.7+-yellow)

A simple, intuitive Python SDK for interacting with the Police Roleplay Community (PRC) API.

## 📋 Features

- Simple, intuitive interface for all PRC API endpoints
- Automatic rate limit handling
- Detailed error information
- Type hints for better IDE integration
- Comprehensive documentation and examples

## 🚀 Installation

```bash
pip install prc-sdk
```

## 🔑 Authentication

The SDK requires a server key for authentication. You can obtain this key from your private server settings in the game.

```python
from prc_sdk import PrcClient

# Initialize with your server key
client = PrcClient(server_key="your-server-key")

# Optionally, you can provide a global API key if you have one
client = PrcClient(
    server_key="your-server-key", 
    api_key="your-global-api-key"
)
```

## 🌟 Quick Examples

### Get Server Status

```python
# Get basic server information
status = client.get_server_status()
print(f"Server Name: {status.name}")
print(f"Players: {status.current_players}/{status.max_players}")
```

### Get Players in Server

```python
# Get all players currently in the server
players = client.get_players()
for player in players:
    print(f"Player: {player.name} | Team: {player.team}")
```

### Execute Command

```python
# Run a command in the server
response = client.execute_command(":h Hello from the Python SDK!")
if response.success:
    print("Command executed successfully")
```

### Get Vehicle Information

```python
# Get all vehicles in the server
vehicles = client.get_vehicles()
for vehicle in vehicles:
    print(f"Vehicle: {vehicle.name} | Owner: {vehicle.owner}")
```

## 📚 Available Methods

### Server Information
- `get_server_status()` - Get basic server information
- `get_players()` - Get all players in the server
- `get_join_logs()` - Get server join logs
- `get_queue()` - Get players in queue
- `get_kill_logs()` - Get kill logs
- `get_command_logs()` - Get command logs
- `get_mod_calls()` - Get moderator call logs
- `get_bans()` - Get server bans
- `get_vehicles()` - Get vehicles in the server

### Server Actions
- `execute_command(command)` - Execute a command as "virtual server management"

## 🚨 Rate Limits

The SDK automatically handles rate limits by respecting the headers provided by the API. If a rate limit is hit, the SDK will wait the appropriate time before retrying the request.

You can configure how the SDK handles rate limits:

```python
from prc_sdk import PrcClient, RateLimitBehavior

client = PrcClient(
    server_key="your-server-key",
    rate_limit_behavior=RateLimitBehavior.WAIT_AND_RETRY  # Default
)

# Other options:
# - RateLimitBehavior.RAISE_EXCEPTION
# - RateLimitBehavior.RETURN_ERROR
```

## ❓ Error Handling

The SDK provides detailed error information via exceptions:

```python
from prc_sdk import PrcClient, PrcApiError

client = PrcClient(server_key="your-server-key")

try:
    status = client.get_server_status()
except PrcApiError as e:
    print(f"Error Code: {e.error_code}")
    print(f"Message: {e.message}")
    print(f"HTTP Status: {e.status_code}")
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🛠️ Maintenance

This repository is maintained by [@zenturocloud](https://github.com/zenturocloud) and is not accepting code requests. However, suggestions and feedback are welcome through issues.

---

Not affiliated with or endorsed by Roblox or Police Roleplay Community.
