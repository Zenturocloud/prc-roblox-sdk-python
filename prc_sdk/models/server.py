"""
Server-related data models for the PRC SDK.
"""


class ServerStatus:
    """Represents the status of a PRC server."""
    
    def __init__(self, data):
        """
        Initialize a new ServerStatus object.
        
        Args:
            data: The server status data from the API.
        """
        self.name = data.get("Name", "")
        self.owner_id = data.get("OwnerId", 0)
        self.current_players = data.get("CurrentPlayers", 0)
        self.max_players = data.get("MaxPlayers", 0)
        self.join_key = data.get("JoinKey", "")
        self.acc_verified_req = data.get("AccVerifiedReq", "")
        self.team_balance = data.get("TeamBalance", False)
        self.co_owner_ids = data.get("CoOwnerIds", [])
    
    def __str__(self):
        """Return a string representation of the server status."""
        return f"{self.name} ({self.current_players}/{self.max_players} players)"
    
    def __repr__(self):
        """Return a detailed string representation of the server status."""
        return (f"ServerStatus(name='{self.name}', owner_id={self.owner_id}, "
                f"current_players={self.current_players}, max_players={self.max_players}, "
                f"join_key='{self.join_key}', acc_verified_req='{self.acc_verified_req}', "
                f"team_balance={self.team_balance}, co_owner_ids={self.co_owner_ids})")
    
    @property
    def is_full(self):
        """Check if the server is full."""
        return self.current_players >= self.max_players


class Vehicle:
    """Represents a vehicle in a PRC server."""
    
    def __init__(self, data):
        """
        Initialize a new Vehicle object.
        
        Args:
            data: The vehicle data from the API.
        """
        self.name = data.get("Name", "")
        self.owner = data.get("Owner", "")
        self.texture = data.get("Texture")
    
    def __str__(self):
        """Return a string representation of the vehicle."""
        return f"{self.name} (Owner: {self.owner})"
    
    def __repr__(self):
        """Return a detailed string representation of the vehicle."""
        return (f"Vehicle(name='{self.name}', owner='{self.owner}', "
                f"texture='{self.texture}')")


class CommandResponse:
    """Represents a response from executing a command in a PRC server."""
    
    def __init__(self, success, status_code, message=None):
        """
        Initialize a new CommandResponse object.
        
        Args:
            success: Whether the command was executed successfully.
            status_code: The HTTPS status code returned by the API.
            message: An optional message explaining the result.
        """
        self.success = success
        self.status_code = status_code
        self.message = message
    
    def __str__(self):
        """Return a string representation of the command response."""
        result = "Success" if self.success else "Failure"
        if self.message:
            result += f": {self.message}"
        return result
    
    def __repr__(self):
        """Return a detailed string representation of the command response."""
        return (f"CommandResponse(success={self.success}, status_code={self.status_code}, "
                f"message='{self.message}')")
