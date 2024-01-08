from controllers.PlayerController import PlayerController
from models.TournamentModel import TournamentModel
from views.loading_screen import loading_screen
from views.good_bye_screen import good_bye_screen
from views.tournament_menu_screen import tournament_menu_screen
from views.show_players_screen import show_players_screen

# from views.tournament_form import tournament_form


class TournamentController:
    """Class to handle tournament related actions"""

    def __init__(self) -> None:
        self.tournament = None

    def create_tournament(self):
        """Function to create a new tournament"""
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
        """Function to load a saved tournament"""
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
        """Function to handle tournament menu options"""
        if self.tournament:
            required_players = self.tournament.round_number * 2
            options = {
                "1": "Afficher les joueurs inscris",
                "2": "Ajouter un joueur",
                "3": f"Commencer le tournoi \
({required_players} joueurs requis)",
            }

            if self.tournament.current_round > 0:
                options = load_options_to_manage()

            options.update(add_options_to_quit())

            while True:
                try:
                    user_choice = tournament_menu_screen(
                        self.tournament, options
                    )
                    if self.tournament.current_round == 0:
                        match user_choice:
                            case "1":
                                show_players_screen(
                                    self.tournament.players,
                                    from_tournament=True,
                                )
                            case "2":
                                contextual_controller = PlayerController()
                                player_to_add = (
                                    contextual_controller.add_player_menu()
                                )
                                if player_to_add.__dict__ not in [
                                    player.__dict__
                                    for player in self.tournament.players
                                ]:
                                    self.tournament.players.append(
                                        player_to_add
                                    )
                                    self.tournament.save()
                                else:
                                    print("Joueur déjà inscris")
                            case "3":
                                if len(self.tournament.players) >= (
                                    self.tournament.round_number * 2
                                ):
                                    # Start tournament
                                    print("Start")
                                else:
                                    # Print error
                                    print(
                                        "Pas assez de joueurs pour commencer"
                                    )
                            case "q":
                                good_bye_screen(
                                    message="Retour au menu principal"
                                )
                                break
                            case _:
                                raise KeyError
                    if self.tournament.current_round > 0:
                        pass
                except KeyError:
                    print(
                        "Aucun choix ne correspond, \
    merci de sélectionner une des options du menu"
                    )
                    continue


def add_options_to_quit():
    """Function to add the save/quit options to a menu"""
    return {
        "q": "Quitter",
    }


def load_options_to_manage():
    """Returns the options to manage a tournament"""
    # Options available when tournament started
    # (overwrite previous choices)
    options = {
        "1": "Afficher les joueurs inscris",
        "2": "Afficher les tours",
        "3": "Inscrire les résultats d'un match",
    }
    return options
