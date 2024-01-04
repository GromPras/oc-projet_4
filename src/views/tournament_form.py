from typing import Dict, Any
from utils import validation


def tournament_form() -> Dict[str, Any]:
    """A function that acts as a form to create a new Tournament"""
    new_tournament = {}
    while True:
        try:
            new_tournament["name"] = validation.field_length(
                value=input("Entrez le nom du tournoi: "), length=2
            )
            break
        except validation.FormValidationError as err:
            print(err)
            continue
    while True:
        try:
            new_tournament["location"] = validation.field_length(
                value=input("Entrez le lieu où se déroule le tournoi: "),
                length=2,
            )
            break
        except validation.FormValidationError as err:
            print(err)
            continue

    while True:
        try:
            new_tournament["starts"] = validation.field_date(
                value=input("Date de début (format: jjmmaaaa): ")
            )
            break
        except validation.FormValidationError as err:
            print(err)
            continue
    while True:
        try:
            new_tournament["ends"] = validation.field_date(
                value=input("Date de fin (format: jjmmaaaa): ")
            )
            break
        except validation.FormValidationError as err:
            print(err)
            continue
    while True:
        try:
            new_tournament["round_number"] = validation.field_number(
                value=input(
                    "En combien de rondes le tournoi se joue? (4 minimum): "
                )
            )
            break
        except validation.FormValidationError as err:
            print(err)
            continue
    while True:
        try:
            new_tournament["description"] = input(
                "Entrez une description si vous le souhaitez: "
            )
            break
        except validation.FormValidationError as err:
            print(err)
            continue

    return new_tournament
