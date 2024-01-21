from models.GameModel import GameModel
from utils.functions import clear_screen


def show_game_screen(game: GameModel) -> None:
    clear_screen()
    print(
        f"{game.player_1.fullname()}({game.player_1_score}) contre \
{game.player_2.fullname()}({game.player_2_score})"
    )

    print()
    input("Appuyez sur la touche [Entrée] pour retourner au menu")
