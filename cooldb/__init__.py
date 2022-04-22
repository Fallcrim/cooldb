import logging

from .db_handler import Session

base_logger = logging.getLogger("cooldb")
base_logger.setLevel(logging.DEBUG)
