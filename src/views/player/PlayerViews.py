from typing import List
from models.PlayerModel import PlayerModel
from utils.functions import clear_screen


class PlayerViews:

    def index(self, players: List[PlayerModel]) -> None:
        """Displays all the players"""
        clear_screen()
        print("Liste des joueurs")
        print("_"*80)
        [self.show(player) for player in players]

    def show(self, player: PlayerModel) -> None:
        """Displays a player"""
        print(player)
