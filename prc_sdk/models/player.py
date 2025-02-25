"""
Player-related data models for the PRC SDK.
"""

from ..utils import extract_player_info


class Player:
    """Represents a player in a PRC server."""
    
    def __init__(self, data):
        """
        Initialize a new Player object.
        
        Args:
            data: The player data from the API.
        """
        player_info = extract_player_info(data.get("Player", ""))
        self.name = player_info["name"]
        self.id = player_info["id"]
        self.permission = data.get("Permission", "")
        self.team = data.get("Team", "")
        self.callsign = data.get("Callsign")
    
    def __str__(self):
        """Return a string representation of the player."""
        if self.callsign:
            return f"{self.name} ({self.callsign})"
        return self.name
    
    def __repr__(self):
        """Return a detailed string representation of the player."""
        return (f"Player(name='{self.name}', id='{self.id}', "
                f"permission='{self.permission}', team='{self.team}', "
                f"callsign='{self.callsign}')")
    
    @property
    def is_admin(self):
        """Check if the player is an administrator."""
        return "Administrator" in self.permission or "Owner" in self.permission
    
    @property
    def is_moderator(self):
        """Check if the player is a moderator."""
        return "Moderator" in self.permission or self.is_admin
    
    @property
    def is_civilian(self):
        """Check if the player is a civilian."""
        return self.team == "Civilian"
