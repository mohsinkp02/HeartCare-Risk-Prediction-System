import logging
import sys
from app.core.config import get_settings

settings = get_settings()

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    return logger

logger = setup_logging()
