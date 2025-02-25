"""
Constants used by the PRC SDK.
"""

# API Base URL
API_BASE_URL = "https://api.policeroleplay.community/v1"

# Error Codes
ERROR_CODES = {
    0: "Unknown error",
    1001: "Error communicating with Roblox / in-game private server",
    1002: "Internal system error",
    2000: "No server-key provided",
    2001: "Incorrectly formatted server-key",
    2002: "Invalid or expired server-key",
    2003: "Invalid global API key",
    2004: "Server-key banned from API access",
    3001: "Invalid command in request body",
    3002: "Server is offline (no players)",
    4001: "Rate limited",
    4002: "Restricted command",
    4003: "Prohibited message",
    9998: "Restricted resource",
    9999: "Out-of-date in-game server module",
}

# Player Permissions
PERMISSION_NORMAL = "Normal"
PERMISSION_MODERATOR = "Server Moderator"
PERMISSION_ADMINISTRATOR = "Server Administrator"
PERMISSION_OWNER = "Server Owner"

# Common Teams
TEAM_CIVILIAN = "Civilian"
TEAM_POLICE = "Police"
TEAM_EMERGENCY = "Emergency Services"
TEAM_FIRE = "Fire Department"
TEAM_EMS = "EMS"

# Default rate limit retry values
DEFAULT_RETRY_AFTER = 60  # seconds
MAX_RETRY_COUNT = 3

# Request timeouts
DEFAULT_TIMEOUT = 10  # seconds
COMMAND_TIMEOUT = 15  # seconds

# Version
SDK_VERSION = "0.1.0"
