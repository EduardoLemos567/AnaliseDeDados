import logging
from logging import StreamHandler
import sys


def setup_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    logger.addHandler(StreamHandler(sys.stdout))
    return logger
