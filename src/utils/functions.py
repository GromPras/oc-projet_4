import calendar
import os
import time
from typing import Literal


ALLOWED_ID_TYPE = Literal["TOURNAMENT", "GAME", "ROUND"]


def clear_screen() -> None:
    # os.system('cls' if os.name == 'nt' else 'clear')
    pass


def generate_id(type: ALLOWED_ID_TYPE) -> str:
    gmt = time.gmtime()
    timestamp = calendar.timegm(gmt)
    return str(f"{type[0]}{timestamp}")


def spacer(length) -> str:
    return " " * length
