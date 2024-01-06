from typing import List
from models.PlayerModel import PlayerModel


def show_tournament_players(players: List[PlayerModel]) -> None:
    if len(players) > 0:
        print(f"{len(players)} joueurs inscris :")
        [print(player) for player in players]
    else:
        print("Aucun joueur n'est inscri")
