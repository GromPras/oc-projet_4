from controllers.PlayerController import PlayerController
from controllers.TournamentController import TournamentController
from views.shared.alert_message import alert_message
from views.shared.loading_screen import loading_screen


app_logo = """
  ____ _                      ____           _
 / ___| |__   ___  ___ ___   / ___|___ _ __ | |_ ___ _ __
| |   | '_ \\ / _ \\/ __/ __| | |   / _ \\ '_ \\| __/ _ \\ '__|
| |___| | | |  __/\\__ \\__ \\ | |__|  __/ | | | ||  __/ |
 \\____|_| |_|\\___||___/___/  \\____\\___|_| |_|\\__\\___|_|

Bienvenue dans ChessCenter, que voulez-vous faire ?
"""


class ApplicationController:
    def index(self) -> None:
        """Home controller for the application
        Gets the user input from a selction of options"""
        tournament_controller = TournamentController()
        player_controller = PlayerController()
        main_menu = {
            "1": {
                "name": "Afficher tous les joueurs",
                "controller": lambda: player_controller.index()
            },
            "2": {
                "name": "Créer un tournoi",
                "controller": lambda: tournament_controller.new()
            },
            "3": {
                "name": "Charger un tournoi",
                "controller": lambda: tournament_controller.load()
            },
            "4": {
                "name": "Afficher un tournoi archivé",
                "controller": lambda: tournament_controller.archives()
            },
            "q": {
                "name": "Quitter",
                "controller": lambda: self.exit_app()
            }
        }
        while True:
            user_choice = loading_screen(
                data={key: option["name"] for key, option in main_menu.items()},
                title=app_logo,
                raw_input=True,
                clear_previous_screen=True
            )
            if user_choice == "q":
                self.exit_app()
                break
            main_menu[user_choice]["controller"]()

    def exit_app(self) -> bool:
        """Exits the application, displaying a nice message."""
        alert_message(
            message="Merci d'avoir utilisé cette application, à bientôt!",
            type="Info"
        )
        return False

    def run(self) -> None:
        self.index()
