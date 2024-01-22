from typing import List, Dict
from models.PlayerModel import PlayerModel
from utils.functions import clear_screen, spacer


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

    def leaderboard(self, players: List[Dict]) -> None:
        sort_by_score = sorted(
            players, key=lambda s: s["player_score"], reverse=True)
        print("Score|     NID| Nom")
        for contender in sort_by_score:
            print(f"""{spacer(length=5-len(str(contender['player_score'])))}\
{contender['player_score']}| \
{contender['player'].national_chess_id}| \
{contender["player"].fullname()}""")
