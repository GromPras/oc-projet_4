from typing import List
from views.show_game_screen import show_game_screen
from models.RoundModel import RoundModel
from utils.functions import clear_screen


def list_rounds_screen(rounds: List[RoundModel]) -> None:
    """Simple view that list games per round"""
    clear_screen()
    for item in rounds:
        if not isinstance(item, RoundModel):
            item = RoundModel(**item)
        print(f"Matchs du {item.name}")
        [show_game_screen(game) for game in item.games]

    print()
    input("Appuyez sur la touche [Entrée] pour retourner au menu")
