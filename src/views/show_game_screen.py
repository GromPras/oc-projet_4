from models.GameModel import GameModel


def show_game_screen(game: GameModel) -> None:
    print(
        f"{game.player_1.fullname()}({game.player_1_score}) contre \
{game.player_2.fullname()}({game.player_2_score})"
    )
