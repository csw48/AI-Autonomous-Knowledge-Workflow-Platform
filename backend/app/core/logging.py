import logging
from typing import Literal

_LOG_LEVELS: dict[str, int] = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def configure_logging(level: Literal[tuple(_LOG_LEVELS.keys())] | str = "INFO") -> None:
    """Configure root logging level once per process."""

    logging.basicConfig(
        level=_LOG_LEVELS.get(level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
