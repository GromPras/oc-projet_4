from models.PlayerModel import PlayerModel
from views.player.PlayerViews import PlayerViews


class PlayerController:
    def __init__(self) -> None:
        self.views = PlayerViews()

    def index(self) -> None:
        """Show every player saved in the db"""
        players = PlayerModel.get_all()
        self.views.index(players=players)
        return

    def show_tournament_players(self, tournament_id: str) -> None:
        """Show players from a specific tournament"""
        print(f"TODO: show tournament: {tournament_id}'s players")
        input("Appuyez sur [Entrée] pour continuer.")

    def add_player_to_tournament(self, tournament_id: str) -> None:
        """Adds a player to a given tournament"""
        print(f"TODO: add player to tournament: {tournament_id}")
        input("Appuyez sur [Entrée] pour continuer.")
