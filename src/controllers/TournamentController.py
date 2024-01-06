from models.TournamentModel import TournamentModel
from views.loading_screen import loading_screen
from views.good_bye_screen import good_bye_screen
from views.tournament_menu_screen import tournament_menu_screen
from views.show_tournament_players import show_tournament_players

# from views.tournament_form import tournament_form


class TournamentController:
    def __init__(self) -> None:
        self.tournament = None

    def create_tournament(self):
        # payload = tournament_form()
        payload = {
            "name": "Echecs et maths",
            "location": "Paris",
            "starts": "18122024",
            "ends": "19202024",
            "description": "",
            "round_number": 4,
        }
        new_tournament = TournamentModel(**payload)
        new_tournament.save()
        self.tournament = new_tournament
        self.tournament_menu()

    def load_tournament(self):
        saved_tournaments = {
            str(index): file
            for index, file in enumerate(TournamentModel.get_all(), 1)
        }
        saved_tournaments["q"] = "Quitter"
        while True:
            try:
                user_choice = saved_tournaments[
                    loading_screen(saved_tournaments)
                ]
                if user_choice == "Quitter":
                    good_bye_screen()
                tournament = TournamentModel.load_by_name(user_choice)
                if not tournament:
                    raise KeyError
                self.tournament = tournament
                break
            except KeyError:
                print(
                    "Aucun choix ne correspond, \
    merci de sélectionner une des options du menu"
                )
                continue
        self.tournament_menu()

    def tournament_menu(self):
        if self.tournament:
            # Default options
            options = {
                "1": "Afficher les joueurs inscris",
                "2": "Ajouter un joueur",
            }

            # Options available when tournament is ready to start
            # (minimum_player >= round_number * 2)
            options_to_start = {
                "3": "Commencer le tournoi",
            }

            # Options available when tournament started
            # (overwrite previous choices)
            options_to_manage = {
                "2": "Afficher les tours",
                "3": "Inscrire les résultats d'un match",
            }

            if self.tournament.current_round == 0 and len(
                self.tournament.players
            ) >= (self.tournament.round_number * 2):
                options.update(options_to_start)
            if self.tournament.current_round > 0:
                options.update(options_to_manage)

            # Add the option to save and quit
            options.update(
                {
                    "s": "Sauvegarder",
                    "q": "Quitter",
                }
            )
            while True:
                try:
                    user_choice = tournament_menu_screen(
                        self.tournament, options
                    )
                    match user_choice:
                        case "1":
                            show_tournament_players(self.tournament.players)
                        case "q":
                            good_bye_screen(message="Retour au menu principal")
                            break
                        case _:
                            raise KeyError
                except KeyError:
                    print(
                        "Aucun choix ne correspond, \
    merci de sélectionner une des options du menu"
                    )
                    continue
