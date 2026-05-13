import logging
import sys
from app.core.config import settings


def setup_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
