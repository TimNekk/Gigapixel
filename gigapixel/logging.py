from enum import Enum
from typing import Optional, Tuple

from loguru import logger


class Level(Enum):
    TRACE = 5
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def log(start: Optional[str] = None,
        end: Optional[str] = None,
        format: Optional[Tuple[int]] = None,
        level: Level = Level.INFO):
    def outer_wrapper(function):
        def wrapper(*args, **kwargs):
            if start:
                format_args = [args[index] for index in (format if format else [])]
                logger.log(level.name, start.format(*format_args))

            result = function(*args, **kwargs)

            if end:
                format_args = [args[index] if index != -1 else result for index in (format if format else [])]
                logger.log(level.name, end.format(*format_args))

            return result

        return wrapper

    return outer_wrapper
