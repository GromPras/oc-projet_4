from models.TournamentModel import TournamentModel
from views.loading_screen import loading_screen
from views.good_bye_screen import good_bye_screen

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
        return self.tournament

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
        return self.tournament

    def tournament_menu(self, tournament):
        self.tournament = tournament
        print(self.tournament)
