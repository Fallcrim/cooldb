import logging

from .sqlite3_session import Session

base_logger = logging.getLogger("cooldb")
base_logger.setLevel(logging.DEBUG)
