# Importing the logging module to configure logging in Python.
import logging

# Function to configure a custom logger.
def logger_conf(name):
    # Create a custom logger with the provided name.
    logger = logging.getLogger(name)

    # Create handlers for the logger.
    c_handler = logging.StreamHandler()  # Handler to output logs to the console.
    f_handler = logging.FileHandler(name + '.log')  # Handler to output logs to a file named after the logger.
    
    # Set the logging levels for the handlers.
    c_handler.setLevel(logging.WARNING)  # Console handler will log warnings and above.
    f_handler.setLevel(logging.ERROR)  # File handler will log errors and above.

    # Create formatters and add them to the handlers.
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')  # Format for console logs.
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Format for file logs.
    c_handler.setFormatter(c_format)  # Add the console formatter to the console handler.
    f_handler.setFormatter(f_format)  # Add the file formatter to the file handler.

    # Add the handlers to the logger.
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    
    # Return the configured logger.
    return logger
