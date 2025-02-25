"""
Client for interacting with the PRC API.
"""

import time
import enum
import requests

from .errors import PrcApiError, PrcConnectionError, PrcRateLimitError, PrcAuthenticationError
from .utils import (
    timestamp_to_datetime, 
    extract_player_info, 
    wait_for_rate_limit, 
    parse_error_response,
    is_valid_server_key,
    make_rate_limit_info
)
from .constants import (
    API_BASE_URL,
    ERROR_CODES,
    DEFAULT_RETRY_AFTER,
    MAX_RETRY_COUNT,
    DEFAULT_TIMEOUT,
    COMMAND_TIMEOUT
)
from .logging import get_logger
from .models.server import ServerStatus, Vehicle, CommandResponse
from .models.player import Player
from .models.logs import JoinLog, KillLog, CommandLog, ModCall


logger = get_logger()


class RateLimitBehavior(enum.Enum):
    """Defines how the client should behave when hitting rate limits."""
    WAIT_AND_RETRY = "wait_and_retry"
    RAISE_EXCEPTION = "raise_exception"
    RETURN_ERROR = "return_error"


class PrcClient:
    """Client for interacting with the PRC API."""
    
    BASE_URL = API_BASE_URL
    
    def __init__(
        self, 
        server_key, 
        api_key=None,
        rate_limit_behavior=RateLimitBehavior.WAIT_AND_RETRY
    ):
        """
        Initialize a new PRC API client.
        
        Args:
            server_key: The server key obtained from the private server settings.
            api_key: Optional global API key for increased rate limits.
            rate_limit_behavior: How the client should handle rate limits.
        """
        self.server_key = server_key
        self.api_key = api_key
        self.rate_limit_behavior = rate_limit_behavior
        self.session = requests.Session()
        self.rate_limit_info = None
        
        logger.debug(f"Initialized PRC client with server key: {server_key[:4]}...")
    
    def _get_headers(self):
        """Get the headers for API requests."""
        headers = {
            "Server-Key": self.server_key
        }
        
        if self.api_key:
            headers["Authorization"] = self.api_key
            
        return headers
    
    def _handle_response(self, response, retry_count=0):
        """
        Handle the API response.
        
        Args:
            response: The response from the API.
            retry_count: The number of times this request has been retried.
            
        Returns:
            The parsed JSON response if successful.
            
        Raises:
            PrcApiError: If the API returns an error.
            PrcRateLimitError: If rate limited and behavior is RAISE_EXCEPTION.
            PrcAuthenticationError: If authentication fails.
            PrcConnectionError: If there's a connection error.
        """
        
        if "X-RateLimit-Limit" in response.headers:
            self.rate_limit_info = make_rate_limit_info(response.headers)
            logger.debug(f"Rate limit info: {self.rate_limit_info}")
        
        if response.status_code == 429:  
            error_data = response.json() if response.content else {"message": "Rate limit exceeded"}
            retry_after = error_data.get("retry_after", DEFAULT_RETRY_AFTER)
            
            logger.warning(f"Rate limited. Retry after: {retry_after} seconds")
            
            if self.rate_limit_behavior == RateLimitBehavior.RAISE_EXCEPTION:
                raise PrcRateLimitError(retry_after=retry_after)
            
            elif self.rate_limit_behavior == RateLimitBehavior.RETURN_ERROR:
                return {
                    "error": True,
                    "message": error_data.get("message", "Rate limit exceeded"),
                    "status_code": 429,
                    "error_code": 4001,
                    "retry_after": retry_after
                }
            
            else:  # WAIT_AND_RETRY
                # Calculate time to wait - either from retry_after or headers
                if "X-RateLimit-Reset" in response.headers:
                    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                    current_time = int(time.time())
                    retry_after = max(1, reset_time - current_time)
                
                # Wait for the rate limit to expire
                logger.info(f"Waiting {retry_after} seconds for rate limit to expire...")
                wait_for_rate_limit(retry_after)
                
                # Retry the request
                if retry_count < MAX_RETRY_COUNT:
                    logger.info(f"Retrying request (attempt {retry_count + 1}/{MAX_RETRY_COUNT})...")
                    return self._handle_request(
                        method=response.request.method,
                        url=response.request.url,
                        json=response.request.json,
                        retry_count=retry_count + 1
                    )
                else:
                    logger.error(f"Max retry count ({MAX_RETRY_COUNT}) exceeded")
                    raise PrcRateLimitError(retry_after=retry_after)
        
        elif response.status_code == 403:  
            error_data = response.json() if response.content else {"message": "Authentication failed"}
            error_code = error_data.get("code", 2003)  
            message = error_data.get("message", "Authentication failed")
            
            logger.error(f"Authentication error: {message} (code: {error_code})")
            raise PrcAuthenticationError(error_code=error_code, message=message)
        
        elif response.status_code >= 400:
            error_data = response.json() if response.content else {"message": "Unknown error"}
            error_code = error_data.get("code", 0)
            message = error_data.get("message", "Unknown error")
            
            logger.error(f"API error: {message} (code: {error_code})")
            raise PrcApiError(
                message=message,
                status_code=response.status_code,
                error_code=error_code
            )
        
        return response.json() if response.content else {}
    
    def _handle_request(self, method, url, json=None, retry_count=0):
        """
        Handle an API request.
        
        Args:
            method: The HTTP method to use.
            url: The URL to send the request to.
            json: Optional JSON data to send with the request.
            retry_count: The number of times this request has been retried.
            
        Returns:
            The parsed JSON response if successful.
            
        Raises:
            PrcApiError: If the API returns an error.
            PrcConnectionError: If there's a connection error.
        """
        headers = self._get_headers()
        
        logger.debug(f"Making {method} request to {url}")
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
            elif method.upper() == "POST":
                response = self.session.post(url, headers=headers, json=json, timeout=COMMAND_TIMEOUT)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection error: {str(e)}")
            raise PrcConnectionError(f"Failed to connect to the PRC API: {str(e)}")
        
        return self._handle_response(response, retry_count)
    
    def get_server_status(self):
        """
        Get information about the server.
        
        Returns:
            A ServerStatus object containing information about the server.
            
        Raises:
            PrcApiError: If the API returns an error.
        """
        url = f"{self.BASE_URL}/server"
        data = self._handle_request("GET", url)
        return ServerStatus(data)
    
    def get_players(self):
        """
        Get all players currently in the server.
        
        Returns:
            A list of Player objects representing the players in the server.
            
        Raises:
            PrcApiError: If the API returns an error.
        """
        url = f"{self.BASE_URL}/server/players"
        data = self._handle_request("GET", url)
        return [Player(player_data) for player_data in data]
    
    def get_join_logs(self):
        """
        Get the join logs for the server.
        
        Returns:
            A list of JoinLog objects representing the join logs.
            
        Raises:
            PrcApiError: If the API returns an error.
        """
        url = f"{self.BASE_URL}/server/joinlogs"
        data = self._handle_request("GET", url)
        return [JoinLog(log_data) for log_data in data]
    
    def get_queue(self):
        """
        Get the IDs of players in the queue.
        
        Returns:
            A list of Roblox IDs of players in the queue.
            
        Raises:
            PrcApiError: If the API returns an error.
        """
        url = f"{self.BASE_URL}/server/queue"
        return self._handle_request("GET", url)
    
    def get_kill_logs(self):
        """
        Get the kill logs for the server.
        
        Returns:
            A list of KillLog objects representing the kill logs.
            
        Raises:
            PrcApiError: If the API returns an error.
        """
        url = f"{self.BASE_URL}/server/killlogs"
        data = self._handle_request("GET", url)
        return [KillLog(log_data) for log_data in data]
    
    def get_command_logs(self):
        """
        Get the command logs for the server.
        
        Returns:
            A list of CommandLog objects representing the command logs.
            
        Raises:
            PrcApiError: If the API returns an error.
        """
        url = f"{self.BASE_URL}/server/commandlogs"
        data = self._handle_request("GET", url)
        return [CommandLog(log_data) for log_data in data]
    
    def get_mod_calls(self):
        """
        Get the moderator call logs for the server.
        
        Returns:
            A list of ModCall objects representing the moderator call logs.
            
        Raises:
            PrcApiError: If the API returns an error.
        """
        url = f"{self.BASE_URL}/server/modcalls"
        data = self._handle_request("GET", url)
        return [ModCall(log_data) for log_data in data]
    
    def get_bans(self):
        """
        Get the bans for the server.
        
        Returns:
            A dictionary mapping player IDs to their names.
            
        Raises:
            PrcApiError: If the API returns an error.
        """
        url = f"{self.BASE_URL}/server/bans"
        return self._handle_request("GET", url)
    
    def get_vehicles(self):
        """
        Get all vehicles in the server.
        
        Returns:
            A list of Vehicle objects representing the vehicles in the server.
            
        Raises:
            PrcApiError: If the API returns an error.
        """
        url = f"{self.BASE_URL}/server/vehicles"
        data = self._handle_request("GET", url)
        return [Vehicle(vehicle_data) for vehicle_data in data]
    
    def execute_command(self, command):
        """
        Execute a command as "virtual server management".
        
        Args:
            command: The command to execute.
            
        Returns:
            A CommandResponse object representing the result of executing the command.
            
        Raises:
            PrcApiError: If the API returns an error.
        """
        url = f"{self.BASE_URL}/server/command"
        json_data = {"command": command}
        
        try:
            self._handle_request("POST", url, json=json_data)
            return CommandResponse(success=True, status_code=200)
        except PrcApiError as e:
            return CommandResponse(
                success=False,
                status_code=e.status_code,
                message=e.message
            )
