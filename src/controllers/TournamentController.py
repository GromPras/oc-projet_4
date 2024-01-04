from models.TournamentModel import TournamentModel

# from views.tournament_form import tournament_form


class TournamentController:
    def __init__(self) -> None:
        self.tournament = None

    def create_tournament(self):
        # payload = tournament_form()
        payload = {
            "name": "Echecs et maths",
            "location": "Paris",
            "starts": "18122023",
            "ends": "19202023",
            "description": "",
            "round_number": 4,
        }
        new_tournament = TournamentModel(**payload)
        print(new_tournament)
