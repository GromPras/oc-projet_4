from models.PlayerModel import PlayerModel
from models.TournamentModel import TournamentModel
from views.player.PlayerViews import PlayerViews
from views.tournament.TournamentViews import TournamentViews
from views.shared.alert_message import alert_message
from views.shared.loading_screen import loading_screen
from utils.errors import LoadError, SaveError


class PlayerController:
    def __init__(self) -> None:
        self.views = PlayerViews()

    def index(self) -> None:
        """Show every player saved in the db"""
        try:
            players = PlayerModel.get_all()
            if players:
                self.views.index(players=players)
                input("Appuyez sur [Entrée] pour continuer.")
            else:
                alert_message(
                    message="Aucun joueur enregistré, ajoutez-en", type="Info"
                )
        except LoadError as e:
            alert_message(message=str(e), type="Error")
        return

    def show_tournament_players(
        self, tournament_id: str, option: str = "leaderboard"
    ) -> None:
        """Show players from a specific tournament"""
        tournament = TournamentModel.load_by_id(tournament_id)
        try:
            tournament_players = PlayerModel.get_tournament_players(
                tournament_id=tournament_id
            )
            if not tournament_players:
                return alert_message(
                    message="Aucun joueur enregistré, ajoutez-en.", type="Info"
                )
            if len(tournament_players) <= 0:
                alert_message(
                    message="Aucun joueur n'est inscrit au tournoi",
                    type="Info",
                )
            else:
                TournamentViews().show(tournament=tournament)
                if option == "leaderboard":
                    self.views.leaderboard(players=tournament_players)
                else:
                    self.views.index(
                        players=[i["player"] for i in tournament_players]
                    )

                input("Appuyez sur [Entrée] pour continuer.")
        except LoadError:
            alert_message(
                message="Aucun fichier de joueurs n'a été trouvé,\
si vous venez de créer le tournoi essayez d'ajouter des joueurs."
            )

    def add_player_to_tournament(self, tournament_id: str) -> None:
        """Adds a player to a given tournament"""
        new_player = self.add_player_menu()
        if not new_player:
            return
        try:
            new_player.save_in_tournament(tournament_id=tournament_id)
            input("Appuyez sur [Entrée] pour continuer.")
        except SaveError as e:
            alert_message(message=str(e), type="Error")

    def add_player_menu(self) -> PlayerModel:
        """Set the options to add a player"""
        options = {
            "1": {
                "name": "Enregistrer un nouveau joueur",
                "controller": lambda: self.register_player(),
            },
            "2": {
                "name": "Charger un joueur depuis la liste",
                "controller": lambda: self.load_player(),
            },
            "q": {
                "name": "Annuler",
                "controller": lambda: alert_message(
                    message="Aucun joueur n'a été ajouté", type="Info"
                ),
            },
        }
        user_choice = loading_screen(
            data={key: option["name"] for key, option in options.items()},
            title="Comment voulez-vous ajouter le joueur ?",
            raw_input=True,
        )
        if user_choice:
            if user_choice == "q" or user_choice == "Annuler":
                return None
            return options[user_choice]["controller"]()

    def register_player(self) -> PlayerModel:
        """Register a new player in the db"""
        payload = self.views.player_form()
        new_player = PlayerModel(**payload)
        try:
            new_player.save()
            return new_player
        except SaveError as e:
            alert_message(message=str(e), type="Error")

    def load_player(self) -> PlayerModel:
        """Load a player from the db"""
        saved_players = PlayerModel.get_all()
        if saved_players:
            player_list = {
                str(index): repr(player)
                for index, player in enumerate(saved_players, 1)
            }
            player_list["q"] = "Annuler"
            selection = loading_screen(
                data=player_list,
                title="Joueurs enregistrés :",
            )
            if selection and selection != "q":
                player = PlayerModel.load_by_id(
                    saved_players[int(selection) - 1].national_chess_id
                )
                return player
            else:
                alert_message(message="Aucun joueur n'a été ajouté")
        else:
            alert_message(
                message="Aucun joueur enregistré, ajoutez-en.", type="Info"
            )
