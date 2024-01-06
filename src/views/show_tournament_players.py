from typing import List
from models.PlayerModel import PlayerModel


def show_tournament_players(players: List[PlayerModel]) -> None:
    print(f"{len(players)} joueurs inscris :")
    [print(player) for player in players]
