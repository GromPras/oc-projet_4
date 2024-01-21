from typing import Dict, Any
from utils import validation


def tournament_form() -> Dict[str, Any]:
    """A function that acts as a form to create a new Tournament"""
    new_tournament = {}

    field_requirements = {
        "name": {
            "prompt": "Entrez le nom du tournoi : ",
            "validation_func": lambda v: validation.field_length(v, 2),
        },
        "location": {
            "prompt": "Lieu où se déroulera le tournoi : ",
            "validation_func": lambda v: validation.field_length(v, 2),
        },
        "starts": {
            "prompt": "Date de début (format : jjmmaaaa) : ",
            "validation_func": lambda v: validation.field_date(v),
        },
        "ends": {
            "prompt": "Date de fin (format : jjmmaaaa) : ",
            "validation_func": lambda v: validation.field_date(v),
        },
        "round_number": {
            "prompt": "En combien de tous le tournoi se joue? (4 minimum) : ",
            "validation_func": lambda v: validation.field_number(v),
        },
        "description": {
            "prompt": "Entrez une description si vous le souhaitez : ",
            "validation_func": None,
        },
    }

    for field, requirements in field_requirements.items():
        if requirements["validation_func"]:
            new_tournament[field] = validation.validate_input(
                requirements["prompt"], requirements["validation_func"]
            )
        else:
            new_tournament[field] = input(requirements["prompt"])

    return new_tournament
