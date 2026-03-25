from __future__ import annotations

import logging
import os
import sys

_VALID_LEVELS: dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """
    Configure root logging once: console (stderr), level from LOG_LEVEL env.

    Invalid or missing LOG_LEVEL defaults to INFO. Safe to call again in tests
    (replaces existing root handlers).
    """
    raw = os.environ.get("LOG_LEVEL")
    if raw is None or not raw.strip():
        level_name = "INFO"
    else:
        level_name = raw.strip().upper()

    level = _VALID_LEVELS.get(level_name, logging.INFO)

    root = logging.getLogger()
    root.setLevel(level)

    for existing in root.handlers[:]:
        root.removeHandler(existing)
        existing.close()

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
    root.addHandler(handler)

    if raw is not None and raw.strip() and level_name not in _VALID_LEVELS:
        _logger.warning("Invalid LOG_LEVEL=%r, using INFO", raw.strip())
