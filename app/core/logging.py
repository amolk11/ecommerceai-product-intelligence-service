import logging
from contextvars import ContextVar
from contextvars import Token
from pathlib import Path

from logging.handlers import RotatingFileHandler

from app.core.config import settings
from app.core.paths import PROJECT_ROOT


request_id_context: ContextVar[str] = ContextVar(
    "request_id",
    default="-",
)


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_context.get()
        return True


def set_request_id(request_id: str) -> Token[str]:
    return request_id_context.set(request_id)


def reset_request_id(token: Token[str]) -> None:
    request_id_context.reset(token)


def _get_log_level() -> int:
    return getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO,
    )


def _get_logs_dir() -> Path:
    log_dir = Path(settings.log_dir)

    if not log_dir.is_absolute():
        log_dir = PROJECT_ROOT / log_dir

    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def get_logger(log_name: str, log_folder: str = "system") -> logging.Logger:

    logger_name = f"{log_folder}.{log_name}"

    logger = logging.getLogger(logger_name)

    if logger.handlers:
        logger.setLevel(_get_log_level())
        return logger

    logger.setLevel(_get_log_level())
    logger.propagate = False

    formatter = logging.Formatter(
        (
            "%(asctime)s | %(levelname)s | %(name)s | "
            "request_id=%(request_id)s | %(message)s"
        )
    )

    request_id_filter = RequestIdFilter()

    if settings.log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(_get_log_level())
        console_handler.setFormatter(formatter)
        console_handler.addFilter(request_id_filter)
        logger.addHandler(console_handler)

    if settings.log_to_file and not settings.is_test:
        log_dir = _get_logs_dir() / log_folder
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"{log_name}.log"

        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=settings.log_file_max_bytes,
            backupCount=settings.log_file_backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(_get_log_level())
        file_handler.setFormatter(formatter)
        file_handler.addFilter(request_id_filter)
        logger.addHandler(file_handler)

    return logger
