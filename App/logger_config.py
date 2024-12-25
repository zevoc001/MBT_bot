import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Create log directory if it doesn't exist
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Path to the log file
log_file = os.path.join(log_dir, 'app.log')

# Set up handler for rotating logs daily
handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=30)
handler.suffix = "%Y-%m-%d"

# Set up formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


# Set up a function to get a logger
def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:  # Avoid adding handler multiple times
        logger.addHandler(handler)
    return logger


# Example usage
if __name__ == "__main__":
    logger = get_logger('my_app')
    logger.info('This is an info message')
    logger.error('This is an error message')
