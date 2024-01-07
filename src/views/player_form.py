from typing import Dict, Any
from utils import validation


def player_form() -> Dict[str, Any]:
    """A function that acts as a form to create a player"""
    new_player = {}
    while True:
        try:
            new_player["first_name"] = validation.field_length(
                value=input("Prénom: "), length=2
            )
            break
        except validation.FormValidationError as err:
            print(err)
            continue

    while True:
        try:
            new_player["last_name"] = validation.field_length(
                value=input("Nom: "), length=2
            )
            break
        except validation.FormValidationError as err:
            print(err)
            continue

    while True:
        try:
            new_player["birth_date"] = validation.field_date(
                value=input("Date de naissance (format: jjmmaaaa): ")
            )
            break
        except validation.FormValidationError as err:
            print(err)
            continue

    while True:
        try:
            new_player["national_chess_id"] = validation.national_chess_id(
                value=input(
                    "Identifiant national d'échecs (format: AA00000): "
                ),
            )
            break
        except validation.FormValidationError as err:
            print(err)
            continue

    return new_player
