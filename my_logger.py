# logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

# Create a custom logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler()  # stdout
file_handler = RotatingFileHandler(os.path.join(os.path.dirname(__file__), 'assistant.log'), maxBytes=50*1024*1024, backupCount=3)  # rotating log file

format_str = '[%(levelname)s] %(asctime)s - %(name)s - %(filename)s - %(message)s'
console_format = logging.Formatter(format_str)
file_format = logging.Formatter(format_str)
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_logger(name):
    return logging.getLogger(name)
