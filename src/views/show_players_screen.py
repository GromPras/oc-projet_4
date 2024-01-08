from typing import List
from models.PlayerModel import PlayerModel


def show_players_screen(
    players: List[PlayerModel], from_tournament=False
) -> None:
    """Displays the given players sorted by last name"""
    if len(players) <= 0:
        if not from_tournament:
            print("Aucun joueur enregistré")
        else:
            print("Aucun joueur inscri")
    else:
        sorted_players = sorted(players, key=lambda k: k.last_name)
        if not from_tournament:
            print("Liste des joueurs : ")
        else:
            print(f"{len(players)} joueurs inscris : ")
        [print(player) for player in sorted_players]
