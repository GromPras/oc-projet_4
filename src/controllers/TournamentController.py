from typing import Any, Dict
from controllers.PlayerController import PlayerController
from models.TournamentModel import TournamentModel
from views.shared.alert_message import alert_message
from views.shared.loading_screen import loading_screen
from views.tournament.TournamentViews import TournamentViews


class TournamentController():
    def __init__(self) -> None:
        self.views = TournamentViews()

    def new(self) -> None:
        """Calls the form to create a tournament
        then save a new Tournament
        and calls the show() function"""
        payload = self.views.new()
        new_tournament = TournamentModel(**payload)
        # TODO: handle errors
        new_tournament.save()
        self.show(new_tournament.id)

    def load(self) -> None:
        """Calls the form to load a saved tournament
        then calls the show() function"""
        saved_tournaments = TournamentModel.get_all()
        load_menu = {
            str(index): tournament.__repr__()
            for index, tournament in enumerate(saved_tournaments, 1)
        }
        load_menu["q"] = "Annuler"
        user_choice = loading_screen(
            data=load_menu, title="Tounois sauvegardés :", raw_input=True
        )
        if user_choice:
            self.show(saved_tournaments[int(user_choice) - 1].get_id())

    def show(self, tournament_id: str) -> None:
        tournament = TournamentModel.load_by_id(tournament_id)
        tournament_menu = self.load_tournament_menu(
            current_round=tournament.current_round,
            tournament_id=tournament.get_id(),
        )
        menu_options = {key: option["name"]
                        for key, option in tournament_menu.items()}
        while True:
            self.views.show(tournament=tournament)
            user_choice = loading_screen(
                data=menu_options,
                title="Que voulez-vous faire ?",
                raw_input=True,
                clear_previous_screen=False
            )
            tournament_menu[user_choice]["controller"]()
            if user_choice == "q" or user_choice == "Quitter":
                alert_message(
                    message="Merci d'avoir utilisé l'application. A bientôt!")
                break
            else:
                continue

    def start_tournament(self, tournament_id: str) -> None:
        """Increment the tournament current round and add a new round to the rounds list"""
        print("TODO: Start tournament")
        input("Appuyez sur [Entrée] pour continuer.")

    def load_tournament_menu(
        self, current_round: int, tournament_id: str
    ) -> Dict[str, Dict[str, Any]]:
        """Returns a menu based on the current round number"""
        menu = {}
        if current_round == 0:
            menu = {
                "1": {
                    "name": "Afficher les joueurs du tournoi",
                    "controller": lambda: PlayerController().show_tournament_players(
                        tournament_id=tournament_id
                    ),
                },
                "2": {
                    "name": "Ajouter un joueur",
                    "controller": lambda: PlayerController().add_player_to_tournament(
                        tournament_id=tournament_id
                    ),
                },
                "3": {
                    "name": "Commencer le tournoi",
                    "controller": lambda: self.start_tournament(
                        tournament_id=tournament_id
                    ),
                },
            }

        menu["q"] = {
            "name": "Quitter",
            "controller": lambda: None
        }
        return menu
