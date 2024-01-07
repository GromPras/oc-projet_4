from typing import List
from models.PlayerModel import PlayerModel


def show_players_screen(players: List[PlayerModel]) -> None:
    if len(players) <= 0:
        print("Aucun joueur enregistré")
    else:
        sorted_players = sorted(players, key=lambda k: k.last_name)
        print("Liste des joueurs : ")
        [print(player) for player in sorted_players]
