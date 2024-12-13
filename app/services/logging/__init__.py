import logging
import logging.handlers

# from app.services.logging.db_handler import LogDBHandler

__all__ = ["init_logger"]


def init_logger(
    log_level: str,
    *,
    enable_console_handler: bool = True,
    enable_db_hanlder: bool = False,
) -> None:
    """Initialize logger with console and db handlers."""
    fmt = (
        "\x1b[32m%(asctime)s\x1b[0m | "
        "%(levelname)-8s\x1b[0m | "
        "\x1b[36m%(name)s\x1b[0m:\x1b[36m%(funcName)s\x1b[0m:\x1b[36m%(lineno)d\x1b[0m - %(message)s"
    )

    date_fmt = "%Y-%m-%d %H:%M:%S"

    if log_level.lower() == "debug":
        level = logging.DEBUG
    else:
        level = logging.INFO

    handlers = []

    if enable_console_handler:
        console_handler = _setup_console_logging(level, fmt, date_fmt)
        handlers.append(console_handler)

    # if enable_db_hanlder:
    #     db_handler = LogDBHandler(logging.INFO, chunk_size=1)
    #     handlers.append(db_handler)

    logging.basicConfig(level=level, handlers=handlers)


def _setup_console_logging(
    level: int,
    fmt: str,
    date_fmt: str,
) -> logging.StreamHandler:
    """Setup console logging."""
    from app.services.logging.formatter import ColorizedFormatter

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(ColorizedFormatter(fmt))
    return console_handler
