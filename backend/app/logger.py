import logging
from logging.handlers import TimedRotatingFileHandler
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# 防止重复添加 handler
if not logger.handlers:

    file_handler = TimedRotatingFileHandler(
        "logs/backend.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))
    logger.addHandler(console_handler)
