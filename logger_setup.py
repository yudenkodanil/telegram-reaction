import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file="bot.log"):
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    # Файл с ротацией
    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    # Консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
