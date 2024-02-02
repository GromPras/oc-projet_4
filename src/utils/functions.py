import calendar
import os
import time
from typing import Literal


ALLOWED_ID_TYPE = Literal["TOURNAMENT", "GAME", "ROUND"]


def clear_screen() -> None:
    """Clear console"""
    os.system("cls" if os.name == "nt" else "clear")


def generate_id(type: ALLOWED_ID_TYPE) -> str:
    """Return a string from a timestamp and a given type"""
    gmt = time.gmtime()
    timestamp = calendar.timegm(gmt)
    return str(f"{type[0]}{timestamp}")


def spacer(length) -> str:
    """Console spacer"""
    return " " * length


def score_to_letter(score: float) -> str:
    if score == 0.0:
        return "D"
    elif score == 0.5:
        return "E"
    elif score == 1.0:
        return "V"
    else:
        return "N/C"
