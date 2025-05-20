import logging
import os

def set_up_logger(
        name:str, 
        *extra_handlers:logging.Handler,
        file_name:str="general_logs.log", 
        file_mode:str="a", 
        format:str="%(asctime)s -- %(levelname)s -- %(module)s -- %(message)s"
        ):
    log_level = os.getenv("LOGGING_LEVEL", "WARNING").upper()  # Get the name of the level
    print(log_level)
    log_level = getattr(logging, log_level, logging.WARNING)  # Get the attribute specified, else, 
        # default to warning
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.hasHandlers():  # In case an already created logger was called
        handler = logging.FileHandler(file_name, mode=file_mode)
        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    for extra in extra_handlers:  # In case the user want to log in any other place than files
        logger.addHandler(extra)

    return logger


