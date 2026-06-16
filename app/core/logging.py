import logging

from logging.handlers import RotatingFileHandler

from app.core.config import settings
from app.core.paths import LOGS_DIR


def get_logger(log_name: str, log_folder: str = "system") -> logging.Logger:

    logger_name = f"{log_folder}.{log_name}"

    logger = logging.getLogger(logger_name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if not settings.is_test:
        log_dir = LOGS_DIR / log_folder
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"{log_name}.log"

        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
