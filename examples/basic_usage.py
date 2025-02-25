"""
Basic usage examples for the PRC SDK.
"""

import time
from datetime import datetime
from typing import List, Dict, Any, Optional

from prc_sdk import (
    PrcClient, 
    RateLimitBehavior, 
    PrcApiError, 
    PrcRateLimitError,
    ServerStatus,
    Player,
    JoinLog,
    KillLog,
    Vehicle
)

# Set your server key here
SERVER_KEY = "your-server-key-here"

def get_server_status() -> None:
    """Example: Get basic server information."""
    
    # Initialize the client
    client = PrcClient(server_key=SERVER_KEY)
    
    try:
        # Get server status
        status: ServerStatus = client.get_server_status()
        
        # Print server information
        print(f"Server Name: {status.name}")
        print(f"Players: {status.current_players}/{status.max_players}")
        print(f"Join Key: {status.join_key}")
        print(f"Account Verification: {status.acc_verified_req}")
        print(f"Team Balance: {status.team_balance}")
        
    except PrcApiError as e:
        print(f"Error: {e}")


def get_players() -> None:
    """Example: Get all players in the server."""
    
    # Initialize the client
    client = PrcClient(server_key=SERVER_KEY)
    
    try:
        # Get players
        players: List[Player] = client.get_players()
        
        # Print player information
        print(f"Total Players: {len(players)}")
        for player in players:
            print(f"\nPlayer: {player.name} (ID: {player.id})")
            print(f"  Permission: {player.permission}")
            print(f"  Team: {player.team}")
            if player.callsign:
                print(f"  Callsign: {player.callsign}")
            
            # Check player properties
            if player.is_admin:
                print("  This player is an administrator")
            elif player.is_moderator:
                print("  This player is a moderator")
            
            if player.is_civilian:
                print("  This player is a civilian")
        
    except PrcApiError as e:
        print(f"Error: {e}")


def get_vehicles() -> None:
    """Example: Get all vehicles in the server."""
    
    # Initialize the client
    client = PrcClient(server_key=SERVER_KEY)
    
    try:
        # Get vehicles
        vehicles: List[Vehicle] = client.get_vehicles()
        
        # Print vehicle information
        print(f"Total Vehicles: {len(vehicles)}")
        for vehicle in vehicles:
            print(f"\nVehicle: {vehicle.name}")
            print(f"  Owner: {vehicle.owner}")
            print(f"  Texture: {vehicle.texture or 'Default'}")
        
    except PrcApiError as e:
        print(f"Error: {e}")


def execute_command() -> None:
    """Example: Execute a command in the server."""
    
    # Initialize the client
    client = PrcClient(server_key=SERVER_KEY)
    
    try:
        # Execute a command
        response = client.execute_command(":h Hello from the PRC SDK!")
        
        # Check if the command was executed successfully
        if response.success:
            print("Command executed successfully!")
        else:
            print(f"Command failed: {response.message} (Status: {response.status_code})")
        
    except PrcApiError as e:
        print(f"Error: {e}")


def rate_limit_handling() -> None:
    """Example: Different ways to handle rate limits."""
    
    # 1. Wait and retry (default)
    client1 = PrcClient(
        server_key=SERVER_KEY,
        rate_limit_behavior=RateLimitBehavior.WAIT_AND_RETRY
    )
    
    # 2. Raise exception
    client2 = PrcClient(
        server_key=SERVER_KEY,
        rate_limit_behavior=RateLimitBehavior.RAISE_EXCEPTION
    )
    
    # 3. Return error
    client3 = PrcClient(
        server_key=SERVER_KEY,
        rate_limit_behavior=RateLimitBehavior.RETURN_ERROR
    )
    
    # Example with exception handling
    try:
        status = client2.get_server_status()
    except PrcRateLimitError as e:
        print(f"Rate limited! Try again in {e.retry_after} seconds")
    except PrcApiError as e:
        print(f"API Error: {e.message}")


if __name__ == "__main__":
    print("=== Server Status ===")
    get_server_status()
    
    print("\n=== Players ===")
    get_players()
    
    print("\n=== Vehicles ===")
    get_vehicles()
    
    print("\n=== Execute Command ===")
    execute_command()
    
    print("\n=== Rate Limit Handling ===")
    rate_limit_handling()
