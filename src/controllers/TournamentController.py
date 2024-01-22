from models.TournamentModel import TournamentModel
from views.tournament.TournamentViews import TournamentViews


class TournamentController:
    def __init__(self) -> None:
        self.views = TournamentViews()

    def new(self) -> None:
        """Calls the form to create a tournament
        then save a new Tournament
        and calls the show() function"""
        payload = self.views.new()
        new_tournament = TournamentModel(**payload)
        new_tournament.save()
        self.show(new_tournament.id)

    def load(self) -> None:
        """Calls the form to load a saved tournament
        then calls the show() function"""
        pass

    def show(self, tournament_id: str) -> None:
        print(tournament_id)
