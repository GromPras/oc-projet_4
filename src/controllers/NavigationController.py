from controllers.TournamentController import TournamentController
from models.TournamentModel import TournamentModel
from views.main_menu import main_menu
from views.good_bye_screen import good_bye_screen


class NavigationController:
    """Controller to manage menus"""

    def __init__(self) -> None:
        self.tournament_data = None

    def main_menu(self) -> TournamentModel | None:
        self.tournament_controller = TournamentController()
        while self.tournament_data is None:
            user_choice = main_menu()
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
                    case "q":
                        good_bye_screen()
                        break
                    case _:
                        raise ValueError
            except ValueError:
                print(
                    "Aucun choix ne correspond, \
merci de sélectionner une des options du menu"
                )
                continue
        self.tournament_controller.tournament_menu(self.tournament_data)
