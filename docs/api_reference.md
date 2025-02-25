# PRC SDK API Reference

This document provides a comprehensive reference for all classes and methods available in the PRC SDK.

## Table of Contents

- [Client](#client)
  - [PrcClient](#prcclient)
  - [RateLimitBehavior](#ratelimitbehavior)
- [Models](#models)
  - [Server Models](#server-models)
  - [Player Models](#player-models)
  - [Log Models](#log-models)
- [Errors](#errors)
- [Utilities](#utilities)

## Client

### PrcClient

The main client class for interacting with the PRC API.

#### Constructor

```python
PrcClient(server_key, api_key=None, rate_limit_behavior=RateLimitBehavior.WAIT_AND_RETRY)
```

**Parameters:**
- `server_key` - The server key obtained from the PRC private server settings.
- `api_key` (optional) - Global API key for increased rate limits.
- `rate_limit_behavior` (optional) - How the client should handle rate limits.

#### Methods

**get_server_status()**

Get information about the server.

```python
status = client.get_server_status()
```

Returns: A `ServerStatus` object.

**get_players()**

Get all players currently in the server.

```python
players = client.get_players()
```

Returns: A list of `Player` objects.

**get_join_logs()**

Get the join logs for the server.

```python
logs = client.get_join_logs()
```

Returns: A list of `JoinLog` objects.

**get_queue()**

Get the IDs of players in the queue.

```python
queue = client.get_queue()
```

Returns: A list of Roblox IDs (integers).

**get_kill_logs()**

Get the kill logs for the server.

```python
logs = client.get_kill_logs()
```

Returns: A list of `KillLog` objects.

**get_command_logs()**

Get the command logs for the server.

```python
logs = client.get_command_logs()
```

Returns: A list of `CommandLog` objects.

**get_mod_calls()**

Get the moderator call logs for the server.

```python
calls = client.get_mod_calls()
```

Returns: A list of `ModCall` objects.

**get_bans()**

Get the bans for the server.

```python
bans = client.get_bans()
```

Returns: A dictionary mapping player IDs to player names.

**get_vehicles()**

Get all vehicles in the server.

```python
vehicles = client.get_vehicles()
```

Returns: A list of `Vehicle` objects.

**execute_command(command)**

Execute a command as "virtual server management".

```python
response = client.execute_command(":h Hello from the PRC SDK!")
```

Parameters:
- `command` - The command to execute.

Returns: A `CommandResponse` object.

### RateLimitBehavior

An enum defining how the client should behave when hitting rate limits.

```python
from prc_sdk import RateLimitBehavior

# Wait and retry automatically (default)
behavior = RateLimitBehavior.WAIT_AND_RETRY

# Raise an exception
behavior = RateLimitBehavior.RAISE_EXCEPTION

# Return an error dictionary
behavior = RateLimitBehavior.RETURN_ERROR
```

## Models

### Server Models

#### ServerStatus

Represents the status of a PRC server.

**Properties:**
- `name` - The name of the server.
- `owner_id` - The ID of the server owner.
- `current_players` - The number of players currently in the server.
- `max_players` - The maximum number of players allowed in the server.
- `join_key` - The join key for the server.
- `acc_verified_req` - The account verification requirement for the server.
- `team_balance` - Whether team balancing is enabled.
- `co_owner_ids` - A list of IDs of co-owners of the server.
- `is_full` - Whether the server is full (current_players >= max_players).

#### Vehicle

Represents a vehicle in a PRC server.

**Properties:**
- `name` - The name of the vehicle.
- `owner` - The name of the player who owns the vehicle.
- `texture` - The texture of the vehicle.

#### CommandResponse

Represents a response from executing a command in a PRC server.

**Properties:**
- `success` - Whether the command was executed successfully.
- `status_code` - The HTTP status code returned by the API.
- `message` - An optional message explaining the result.

### Player Models

#### Player

Represents a player in a PRC server.

**Properties:**
- `name` - The name of the player.
- `id` - The ID of the player.
- `permission` - The permission level of the player.
- `team` - The team the player is on.
- `callsign` - The callsign of the player (if any).
- `is_admin` - Whether the player is an administrator.
- `is_moderator` - Whether the player is a moderator.
- `is_civilian` - Whether the player is a civilian.

### Log Models

#### JoinLog

Represents a join log entry in a PRC server.

**Properties:**
- `join` - Whether the log entry represents a join (True) or leave (False).
- `timestamp` - The Unix timestamp when the event occurred.
- `datetime` - The datetime object representing the timestamp.
- `player_name` - The name of the player.
- `player_id` - The ID of the player.

#### KillLog

Represents a kill log entry in a PRC server.

**Properties:**
- `killed_name` - The name of the player who was killed.
- `killed_id` - The ID of the player who was killed.
- `killer_name` - The name of the player who killed.
- `killer_id` - The ID of the player who killed.
- `timestamp` - The Unix timestamp when the event occurred.
- `datetime` - The datetime object representing the timestamp.

#### CommandLog

Represents a command log entry in a PRC server.

**Properties:**
- `player_name` - The name of the player who executed the command.
- `player_id` - The ID of the player who executed the command.
- `timestamp` - The Unix timestamp when the command was executed.
- `datetime` - The datetime object representing the timestamp.
- `command` - The command that was executed.

#### ModCall

Represents a moderator call log entry in a PRC server.

**Properties:**
- `caller_name` - The name of the player who called a moderator.
- `caller_id` - The ID of the player who called a moderator.
- `timestamp` - The Unix timestamp when the call was made.
- `datetime` - The datetime object representing the timestamp.
- `moderator_name` - The name of the moderator who responded (if any).
- `moderator_id` - The ID of the moderator who responded (if any).

## Errors

### PrcError

Base exception for all PRC errors.

### PrcApiError

Exception raised for PRC API errors.

**Properties:**
- `message` - The error message.
- `status_code` - The HTTP status code.
- `error_code` - The PRC error code.

### PrcConnectionError

Exception raised for connection errors.

**Properties:**
- `message` - The error message.

### PrcRateLimitError

Exception raised for rate limit errors.

**Properties:**
- `message` - The error message.
- `status_code` - The HTTP status code (429).
- `error_code` - The PRC error code (4001).
- `retry_after` - The number of seconds to wait before retrying.

### PrcAuthenticationError

Exception raised for authentication errors.

**Properties:**
- `message` - The error message.
- `status_code` - The HTTP status code (403).
- `error_code` - The specific authentication error code.

## Utilities

### timestamp_to_datetime(timestamp)

Convert a Unix timestamp to a datetime object.

```python
from prc_sdk import timestamp_to_datetime

dt = timestamp_to_datetime(1704614400)
```

### datetime_to_timestamp(dt)

Convert a datetime object to a Unix timestamp.

```python
from prc_sdk import datetime_to_timestamp
from datetime import datetime

ts = datetime_to_timestamp(datetime.now())
```

### extract_player_info(player_string)

Extract player name and ID from a player string.

```python
from prc_sdk.utils import extract_player_info

info = extract_player_info("PlayerName:123456")
# info = {"name": "PlayerName", "id": "123456"}
```

### format_datetime(dt, format_string="%Y-%m-%d %H:%M:%S")

Format a datetime object as a string.

```python
from prc_sdk import format_datetime
from datetime import datetime

formatted = format_datetime(datetime.now())
```
