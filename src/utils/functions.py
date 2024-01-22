import calendar
import os
import time


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def generate_id() -> str:
    gmt = time.gmtime()
    timestamp = calendar.timegm(gmt)
    return str(f"T{timestamp}")
