from typing import Any, Dict
from models.TournamentModel import TournamentModel
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

    def show(
        self,
        tournament: TournamentModel
    ) -> str:
        clear_screen()
        print(f"""
{tournament.name}
[{tournament.location}] Du {tournament.starts} au {tournament.ends}
Se joue en {tournament.number_of_rounds} tours. Tour actuel : {tournament.current_round}
""")
        if tournament.description != "":
            print(tournament.description)
        print("_"*80)

    def archive(self, archived_tournament: Dict) -> None:
        print(f"""
{archived_tournament["name"]}
[{archived_tournament["location"]}] Du {archived_tournament["starts"]} au {archived_tournament["ends"]}
S'est joué en {archived_tournament["number_of_rounds"]} tours
""")
        if archived_tournament["description"] != "":
            print(archived_tournament["description"])
        print("_"*80)
        print("Classement : ")
        for p in archived_tournament["players"]:
            print(f"""
{p["player"]["first_name"]} {p["player"]["last_name"]} #{p["player"]["national_chess_id"]} - {p["player_score"]} points""")
        print("_"*80)
        print("Matchs : ")
        for index, r in enumerate(sorted(archived_tournament["rounds"], key= lambda r: r["name"]), 1):
            print(f"""{r["name"]} Début: {r["started_on"].split('.')[0]} - Fin: {r["ended_on"].split('.')[0]}""")
            print("-"*40)
            for g in r["games"]:
                print(f"""{g["player_1"]} (score: {g["player_1_score"]}) \
contre {g["player_2"]} (score: {g["player_2_score"]})""")
            if index < len(archived_tournament["rounds"]):
                print("-"*40)