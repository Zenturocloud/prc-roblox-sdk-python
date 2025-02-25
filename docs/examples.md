# PRC SDK Examples

This document provides examples of how to use the PRC SDK for common tasks.

## Table of Contents

- [Installation](#installation)
- [Basic Client Setup](#basic-client-setup)
- [Getting Server Information](#getting-server-information)
- [Working with Players](#working-with-players)
- [Server Logs](#server-logs)
- [Vehicle Information](#vehicle-information)
- [Executing Commands](#executing-commands)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## Installation

Install the PRC SDK using pip:

```bash
pip install prc-sdk
```

## Basic Client Setup

Import the PRC SDK and initialize a client:

```python
from src import PrcClient

# Initialize with your server key
client = PrcClient(server_key="your-server-key-here")

# Optionally, provide a global API key for increased rate limits
client = PrcClient(
    server_key="your-server-key-here",
    api_key="your-global-api-key"
)
```

## Getting Server Information

Retrieve basic information about your server:

```python
# Get server status
status = client.get_server_status()

# Access server properties
print(f"Server Name: {status.name}")
print(f"Players: {status.current_players}/{status.max_players}")
print(f"Join Key: {status.join_key}")
print(f"Account Verification: {status.acc_verified_req}")
print(f"Team Balance: {status.team_balance}")

# Check if the server is full
if status.is_full:
    print("Server is full!")
else:
    print(f"Server has {status.max_players - status.current_players} slots available")
```

## Working with Players

Get a list of players currently in the server:

```python
# Get all players
players = client.get_players()

# Print basic player information
print(f"Total Players: {len(players)}")
for player in players:
    print(f"Player: {player.name} (ID: {player.id})")
    print(f"  Team: {player.team}")
    if player.callsign:
        print(f"  Callsign: {player.callsign}")

# Filter players by team
police_officers = [p for p in players if p.team == "Police"]
civilians = [p for p in players if p.is_civilian]

print(f"Police Officers: {len(police_officers)}")
print(f"Civilians: {len(civilians)}")

# Filter players by permission
admins = [p for p in players if p.is_admin]
moderators = [p for p in players if p.is_moderator]

print(f"Administrators: {len(admins)}")
print(f"Moderators: {len(moderators)}")
```

Get players in the queue:

```python
# Get queue
queue = client.get_queue()
print(f"Players in queue: {len(queue)}")
```

## Server Logs

### Join Logs

```python
# Get join logs
join_logs = client.get_join_logs()

# Print join/leave events
for log in join_logs:
    action = "joined" if log.join else "left"
    time_str = log.datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_str}: {log.player_name} {action} the server")
```

### Kill Logs

```python
# Get kill logs
kill_logs = client.get_kill_logs()

# Print kill events
for log in kill_logs:
    time_str = log.datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_str}: {log.killer_name} killed {log.killed_name}")
```

### Command Logs

```python
# Get command logs
command_logs = client.get_command_logs()

# Print command executions
for log in command_logs:
    time_str = log.datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_str}: {log.player_name} executed: {log.command}")
```

### Moderator Call Logs

```python
# Get moderator call logs
mod_calls = client.get_mod_calls()

# Print moderator calls
for call in mod_calls:
    time_str = call.datetime.strftime("%Y-%m-%d %H:%M:%S")
    if call.moderator_name:
        print(f"{time_str}: {call.caller_name} called a moderator, responded by {call.moderator_name}")
    else:
        print(f"{time_str}: {call.caller_name} called a moderator (unresponded)")
```

## Vehicle Information

Get a list of vehicles in the server:

```python
# Get all vehicles
vehicles = client.get_vehicles()

# Print vehicle information
print(f"Total Vehicles: {len(vehicles)}")
for vehicle in vehicles:
    print(f"Vehicle: {vehicle.name}")
    print(f"  Owner: {vehicle.owner}")
    print(f"  Texture: {vehicle.texture or 'Default'}")

# Filter vehicles by owner
player_vehicles = {}
for vehicle in vehicles:
    if vehicle.owner not in player_vehicles:
        player_vehicles[vehicle.owner] = []
    player_vehicles[vehicle.owner].append(vehicle)

# Print vehicles by owner
for owner, vehicles in player_vehicles.items():
    print(f"{owner} has {len(vehicles)} vehicles:")
    for vehicle in vehicles:
        print(f"  - {vehicle.name}")
```

## Executing Commands

Execute commands in the server:

```python
# Send a message to all players
response = client.execute_command(":h Hello from the PRC SDK!")

# Check if the command was successful
if response.success:
    print("Message sent successfully!")
else:
    print(f"Failed to send message: {response.message}")

# Kick a player
response = client.execute_command(":k PlayerName Kicked for testing")

# Ban a player
response = client.execute_command(":ban PlayerName Banned for testing")

# Warn a player
response = client.execute_command(":warn PlayerName Please follow the rules")
```

## Error Handling

Handle errors that might occur when using the SDK:

```python
from src import PrcClient, PrcApiError, PrcRateLimitError, PrcConnectionError, PrcAuthenticationError

client = PrcClient(server_key="your-server-key-here")

try:
    status = client.get_server_status()
    print(f"Server Name: {status.name}")
    
except PrcAuthenticationError as e:
    print(f"Authentication Error: {e.message}")
    print(f"Make sure your server key is correct")
    
except PrcRateLimitError as e:
    print(f"Rate Limited: {e.message}")
    print(f"Try again in {e.retry_after} seconds")
    
except PrcConnectionError as e:
    print(f"Connection Error: {e.message}")
    print("Check your internet connection")
    
except PrcApiError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
    print(f"Error Code: {e.error_code}")
```

## Rate Limiting

Configure how the client handles rate limits:

```python
from src import PrcClient, RateLimitBehavior

# Wait and retry automatically (default)
client = PrcClient(
    server_key="your-server-key",
    rate_limit_behavior=RateLimitBehavior.WAIT_AND_RETRY
)

# Raise an exception
client = PrcClient(
    server_key="your-server-key",
    rate_limit_behavior=RateLimitBehavior.RAISE_EXCEPTION
)

# Return an error dictionary
client = PrcClient(
    server_key="your-server-key",
    rate_limit_behavior=RateLimitBehavior.RETURN_ERROR
)
```

When using `RAISE_EXCEPTION`, handle the rate limit exception:

```python
from src import PrcClient, RateLimitBehavior, PrcRateLimitError

client = PrcClient(
    server_key="your-server-key",
    rate_limit_behavior=RateLimitBehavior.RAISE_EXCEPTION
)

try:
    status = client.get_server_status()
except PrcRateLimitError as e:
    print(f"Rate limited! Try again in {e.retry_after} seconds")
    # Wait and retry manually
    import time
    time.sleep(e.retry_after)
    status = client.get_server_status()
```

When using `RETURN_ERROR`, check the response for errors:

```python
from src import PrcClient, RateLimitBehavior

client = PrcClient(
    server_key="your-server-key",
    rate_limit_behavior=RateLimitBehavior.RETURN_ERROR
)

response = client.get_server_status()
if isinstance(response, dict) and response.get("error"):
    print(f"Error: {response.get('message')}")
    if response.get("status_code") == 429:
        print(f"Rate limited! Try again in {response.get('retry_after')} seconds")
else:
    print(f"Server Name: {response.name}")
```
