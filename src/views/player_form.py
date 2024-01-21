from typing import Dict, Any
from utils import validation


def player_form() -> Dict[str, Any]:
    """A function that acts as a form to create a player"""
    new_player = {}

    fields_requirements = {
        "first_name": {
            "prompt": "Prénom : ",
            "validation_func": lambda v: validation.field_length(v, 2),
        },
        "last_name": {
            "prompt": "Nom : ",
            "validation_func": lambda v: validation.field_length(v, 2),
        },
        "birth_date": {
            "prompt": "Date de naissance (format: jjmmaaaa) : ",
            "validation_func": lambda v: validation.field_date(v),
        },
        "national_chess_id": {
            "prompt": "Identifiant national d'échecs (format: AA00000) : ",
            "validation_func": lambda v: validation.national_chess_id(v),
        },
    }

    for field, requirements in fields_requirements.items():
        new_player[field] = validation.validate_input(
            requirements["prompt"], requirements["validation_func"]
        )

    return new_player
