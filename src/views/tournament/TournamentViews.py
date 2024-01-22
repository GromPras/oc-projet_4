from typing import Any, Dict
from utils.functions import clear_screen
from utils import validation


class TournamentViews:
    def new(self) -> Dict[str, Any]:
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
            "number_of_rounds": {
                "prompt": "En combien de tous le tournoi se joue? (4 minimum) : ",
                "validation_func": lambda v: validation.field_number(v),
            },
            "description": {
                "prompt": "Entrez une description si vous le souhaitez : ",
                "validation_func": None,
            },
        }

        clear_screen()
        print("Création d'un tournoi :")
        print("_"*80)

        new_tournament = {}
        for field, requirements in field_requirements.items():
            if requirements["validation_func"]:
                new_tournament[field] = validation.validate_input(
                    requirements["prompt"],
                    requirements["validation_func"]
                )
            else:
                new_tournament[field] = input(requirements["prompt"])

        return new_tournament

    def show(self, tournament) -> None:
        clear_screen()
        print(f"""
{tournament.id} - {tournament.name}
[{tournament.location}] Du {tournament.starts} au {tournament.ends}
Se joue en {tournament.number_of_rounds} tours.
Tour actuel : {tournament.current_round}
{tournament.description if not None else ""}
""")
