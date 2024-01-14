from controllers.TournamentController import TournamentController
from controllers.PlayerController import PlayerController
from models.TournamentModel import TournamentModel
from views.main_menu_screen import main_menu_screen
from views.good_bye_screen import good_bye_screen
from views.alert_message import alert_message


class NavigationController:
    """Controller to manage menus"""

    def __init__(self) -> None:
        self.tournament_data = None

    def main_menu(self) -> TournamentModel | None:
        """Displays the main options when starting the program"""
        self.tournament_controller = TournamentController()
        while self.tournament_data is None:
            user_choice = main_menu_screen()
            try:
                match user_choice:
                    case "1":
                        self.tournament_data = (
                            self.tournament_controller.create_tournament()
                        )
                    case "2":
                        self.tournament_data = (
                            self.tournament_controller.load_tournament()
                        )
                    case "3":
                        PlayerController.show_players()
                    case "q":
                        good_bye_screen()
                        break
                    case _:
                        raise ValueError
            except ValueError:
                alert_message(
                    message="Aucun choix ne correspond, \
merci de sélectionner une des options du menu",
                    type="Error",
                )
                continue
