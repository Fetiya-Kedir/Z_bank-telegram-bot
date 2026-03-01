from __future__ import annotations

import logging


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure a consistent application logger.
    python-telegram-bot uses the standard logging module, so this controls bot logs too.
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )