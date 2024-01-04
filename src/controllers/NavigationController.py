from controllers.TournamentController import TournamentController
from models.TournamentModel import TournamentModel
from views.main_menu import main_menu
from views.good_bye_screen import good_bye_screen


class NavigationController:
    """Controller to manage menus"""

    def main_menu(self) -> TournamentModel | None:
        self.tournament = TournamentController()
        while True:
            user_choice = main_menu()
            try:
                match user_choice:
                    case "1":
                        return self.tournament.create_tournament()
                    case "2":
                        return self.tournament.load_tournament()
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
