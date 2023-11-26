import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = os.getenv('LOG_DIR', '/app/log')
LOG_FILE = 'simulate_logs.log'
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)


def setup_custom_logger():
    logger = logging.getLogger('SIMULATOR')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(name)s | [%(asctime)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = TimedRotatingFileHandler(
        LOG_PATH, when='midnight', interval=1, backupCount=7
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
