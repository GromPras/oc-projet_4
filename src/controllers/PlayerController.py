from models.PlayerModel import PlayerModel
from models.TournamentModel import TournamentModel
from views.player.PlayerViews import PlayerViews
from views.tournament.TournamentViews import TournamentViews
from views.shared.alert_message import alert_message
from utils.errors import LoadError


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
        tournament = TournamentModel.load_by_id(tournament_id)
        try:
            tournament_players = PlayerModel.get_tournament_players(
                tournament_id=tournament_id
            )
            if len(tournament_players) <= 0:
                alert_message(
                    message="Aucun joueur n'est inscrit au tournoi", type="Info")
            else:
                TournamentViews().show(tournament=tournament)
                self.views.leaderboard(players=tournament_players)

                input("Appuyez sur [Entrée] pour continuer.")
        except LoadError:
            alert_message(
                message="Aucun fichier de joueurs n'a été trouvé, si vous venez de créer le tournoi essayez d'ajouter des joueurs.")

    def add_player_to_tournament(self, tournament_id: str) -> None:
        """Adds a player to a given tournament"""
        print(f"TODO: add player to tournament: {tournament_id}")
        input("Appuyez sur [Entrée] pour continuer.")
