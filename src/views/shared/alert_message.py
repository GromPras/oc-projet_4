from typing import Literal


ALLOWED_TYPES = Literal["Info", "Error"]


def alert_message(message: str, type: ALLOWED_TYPES = "Info") -> None:
    """Prints a message in the console formated according to its type
    type: ALLOWED_TYPES = Literal["Info", "Error"]
    """
    print(message)

    print()
    input("Appuyez sur la touche [Entrée] pour continuer.")
