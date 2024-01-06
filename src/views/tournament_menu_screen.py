from typing import Dict
from models.TournamentModel import TournamentModel


def tournament_menu_screen(
    tournament: TournamentModel, options: Dict[str, str]
) -> str:
    """Function to display tournament related options"""
    print(tournament)
    [print(f"{key}: {options[key]}") for key in options.keys()]
    return input("Que voulez-vous faire ?: ")
