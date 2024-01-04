from models.TournamentModel import TournamentModel
from views.main_menu import main_menu
from views.good_bye_screen import good_bye_screen
from views.loading_screen import loading_screen
from views.tournament_form import tournament_form


class NavigationController:
    """Controller to manage menus"""

    def main_menu(self) -> TournamentModel | None:
        while True:
            user_choice = main_menu()
            try:
                match user_choice:
                    case "1":
                        return tournament_form()
                    case "2":
                        return loading_screen(data=TournamentModel.get_all())
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
