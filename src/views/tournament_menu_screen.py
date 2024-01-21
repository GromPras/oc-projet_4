from typing import Dict
from models.TournamentModel import TournamentModel
from utils.functions import clear_screen


def tournament_menu_screen(
    tournament: TournamentModel, options: Dict[str, str]
) -> str:
    """Function to display tournament related options"""
    clear_screen()
    print(tournament)
    [print(f"{key}: {options[key]}") for key in options.keys()]
    return input("Que voulez-vous faire ?: ")
