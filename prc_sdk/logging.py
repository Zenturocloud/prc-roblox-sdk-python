"""
Logging configuration for the PRC SDK.
"""

import logging
import sys


logger = logging.getLogger("prc_sdk")

def configure_logging(
    level=logging.INFO,
    format_string=None,
    stream_handler=True,
    file_handler=None
):
    """
    Configure logging for the PRC SDK.
    
    Args:
        level: The logging level to use.
        format_string: The format string to use for log messages.
        stream_handler: Whether to log to stdout/stderr.
        file_handler: An optional file path to log to.
        
    Returns:
        The configured logger instance.
    """
    
    logger.handlers = []
    
   
    logger.setLevel(level)
    
   
    if format_string is None:
        format_string = "[%(asctime)s] %(levelname)s - %(name)s: %(message)s"
    formatter = logging.Formatter(format_string)
    
    
    if stream_handler:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    
    
    if file_handler:
        file_handler_obj = logging.FileHandler(file_handler)
        file_handler_obj.setFormatter(formatter)
        logger.addHandler(file_handler_obj)
    
    return logger


def disable_logging():
    """Disable all logging for the PRC SDK."""
    logger.handlers = []
    logger.addHandler(logging.NullHandler())
    logger.propagate = False


def get_logger():
    """Get the PRC SDK logger."""
    return logger
