# utils/logger.py
import logging
import os

def setup_logger(name: str, log_file: str = "logs/app.log", level=logging.INFO):
    """Function to setup a logger with file and console handlers"""
    
    # Ensure logs directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False  # Prevent duplicate logs

    return logger