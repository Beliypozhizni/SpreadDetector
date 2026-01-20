import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(
        name: str = "app",
        log_level: str = "INFO",
        log_to_file: bool = True,
        log_file: str = "logs/app.log",
        max_file_size: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 5
) -> logging.Logger:
    """
    Logger configuration for the entire application
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    logger.handlers.clear()

    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_to_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


app_logger = setup_logger()

logger = app_logger
