"""
Log-related data models for the PRC SDK.
"""

from ..utils import extract_player_info, timestamp_to_datetime


class JoinLog:
    """Represents a join log entry in a PRC server."""
    
    def __init__(self, data):
        """
        Initialize a new JoinLog object.
        
        Args:
            data: The join log data from the API.
        """
        self.join = data.get("Join", False)
        self.timestamp = data.get("Timestamp", 0)
        self.datetime = timestamp_to_datetime(self.timestamp)
        
        player_info = extract_player_info(data.get("Player", ""))
        self.player_name = player_info["name"]
        self.player_id = player_info["id"]
    
    def __str__(self):
        """Return a string representation of the join log."""
        action = "joined" if self.join else "left"
        time_str = self.datetime.strftime("%Y-%m-%d %H:%M:%S")
        return f"{time_str}: {self.player_name} {action} the server"
    
    def __repr__(self):
        """Return a detailed string representation of the join log."""
        return (f"JoinLog(player_name='{self.player_name}', player_id='{self.player_id}', "
                f"join={self.join}, timestamp={self.timestamp}, "
                f"datetime='{self.datetime}')")


class KillLog:
    """Represents a kill log entry in a PRC server."""
    
    def __init__(self, data):
        """
        Initialize a new KillLog object.
        
        Args:
            data: The kill log data from the API.
        """
        killed_info = extract_player_info(data.get("Killed", ""))
        self.killed_name = killed_info["name"]
        self.killed_id = killed_info["id"]
        
        killer_info = extract_player_info(data.get("Killer", ""))
        self.killer_name = killer_info["name"]
        self.killer_id = killer_info["id"]
        
        self.timestamp = data.get("Timestamp", 0)
        self.datetime = timestamp_to_datetime(self.timestamp)
    
    def __str__(self):
        """Return a string representation of the kill log."""
        time_str = self.datetime.strftime("%Y-%m-%d %H:%M:%S")
        return f"{time_str}: {self.killer_name} killed {self.killed_name}"
    
    def __repr__(self):
        """Return a detailed string representation of the kill log."""
        return (f"KillLog(killer_name='{self.killer_name}', killer_id='{self.killer_id}', "
                f"killed_name='{self.killed_name}', killed_id='{self.killed_id}', "
                f"timestamp={self.timestamp}, datetime='{self.datetime}')")


class CommandLog:
    """Represents a command log entry in a PRC server."""
    
    def __init__(self, data):
        """
        Initialize a new CommandLog object.
        
        Args:
            data: The command log data from the API.
        """
        player_info = extract_player_info(data.get("Player", ""))
        self.player_name = player_info["name"]
        self.player_id = player_info["id"]
        
        self.timestamp = data.get("Timestamp", 0)
        self.datetime = timestamp_to_datetime(self.timestamp)
        self.command = data.get("Command", "")
    
    def __str__(self):
        """Return a string representation of the command log."""
        time_str = self.datetime.strftime("%Y-%m-%d %H:%M:%S")
        return f"{time_str}: {self.player_name} executed: {self.command}"
    
    def __repr__(self):
        """Return a detailed string representation of the command log."""
        return (f"CommandLog(player_name='{self.player_name}', player_id='{self.player_id}', "
                f"command='{self.command}', timestamp={self.timestamp}, "
                f"datetime='{self.datetime}')")


class ModCall:
    """Represents a moderator call log entry in a PRC server."""
    
    def __init__(self, data):
        """
        Initialize a new ModCall object.
        
        Args:
            data: The moderator call log data from the API.
        """
        caller_info = extract_player_info(data.get("Caller", ""))
        self.caller_name = caller_info["name"]
        self.caller_id = caller_info["id"]
        
        self.timestamp = data.get("Timestamp", 0)
        self.datetime = timestamp_to_datetime(self.timestamp)
        
        moderator = data.get("Moderator")
        if moderator:
            moderator_info = extract_player_info(moderator)
            self.moderator_name = moderator_info["name"]
            self.moderator_id = moderator_info["id"]
        else:
            self.moderator_name = None
            self.moderator_id = None
    
    def __str__(self):
        """Return a string representation of the moderator call log."""
        time_str = self.datetime.strftime("%Y-%m-%d %H:%M:%S")
        if self.moderator_name:
            return f"{time_str}: {self.caller_name} called a moderator, responded by {self.moderator_name}"
        return f"{time_str}: {self.caller_name} called a moderator (unresponded)"
    
    def __repr__(self):
        """Return a detailed string representation of the moderator call log."""
        return (f"ModCall(caller_name='{self.caller_name}', caller_id='{self.caller_id}', "
                f"moderator_name='{self.moderator_name}', moderator_id='{self.moderator_id}', "
                f"timestamp={self.timestamp}, datetime='{self.datetime}')")
