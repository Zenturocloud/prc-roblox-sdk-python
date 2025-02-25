"""
PRC SDK - A Python SDK for interacting with the PRC API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A simple, intuitive Python SDK for interacting with the Police Roleplay Community (PRC) API.

:copyright: (c) 2025 by zenturocloud
:license: MIT, see LICENSE for more details.
"""

__title__ = 'prc_sdk'
__version__ = '0.1.0'
__author__ = 'zenturocloud'
__license__ = 'MIT'
__copyright__ = 'Copyright 2025 zenturocloud'


from .client import PrcClient, RateLimitBehavior


from .errors import (
    PrcError,
    PrcApiError,
    PrcConnectionError,
    PrcRateLimitError,
    PrcAuthenticationError,
)


from .models.server import ServerStatus, Vehicle, CommandResponse
from .models.player import Player
from .models.logs import JoinLog, KillLog, CommandLog, ModCall


from .utils import (
    timestamp_to_datetime,
    datetime_to_timestamp,
    extract_player_info,
    format_datetime,
)

__all__ = [
    
    'PrcClient',
    'RateLimitBehavior',
    
    
    'ServerStatus',
    'Vehicle',
    'CommandResponse',
    
    
    'Player',
    
   
    'JoinLog',
    'KillLog',
    'CommandLog',
    'ModCall',
    
    
    'PrcError',
    'PrcApiError',
    'PrcConnectionError',
    'PrcRateLimitError',
    'PrcAuthenticationError',
    
    
    'timestamp_to_datetime',
    'datetime_to_timestamp',
    'extract_player_info',
    'format_datetime',
]
