import logging

from .sqlite3_session import Session
from .aiosqlite_session import AsyncSession

base_logger = logging.getLogger("cooldb")
base_logger.setLevel(logging.DEBUG)
