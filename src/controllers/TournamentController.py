from models.TournamentModel import TournamentModel
from views.shared.loading_screen import loading_screen
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
            data=load_menu,
            title="Tounois sauvegardés :",
            raw_input=True
        )
        if user_choice:
            self.show(saved_tournaments[int(user_choice) - 1].id)

    def show(self, tournament_id: str) -> None:
        print(tournament_id)
        tournament = TournamentModel.load_by_id(f"{tournament_id}.json")
        self.views.show(tournament=tournament)
