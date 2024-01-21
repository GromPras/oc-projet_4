from typing import List
from controllers.PlayerController import PlayerController
from controllers.RoundController import RoundController
from models.TournamentModel import TournamentModel
from models.PlayerModel import PlayerModel
from views.loading_screen import loading_screen
from views.good_bye_screen import good_bye_screen
from views.tournament_menu_screen import tournament_menu_screen
from views.show_players_screen import show_players_screen
from views.tournament_form import tournament_form
from views.list_rounds_screen import list_rounds_screen
from views.alert_message import alert_message


class TournamentController:
    """Class to handle tournament related actions"""

    def __init__(self) -> None:
        self.tournament = None

    def create_tournament(self) -> None:
        """Function to create a new tournament"""
        payload = tournament_form()
        new_tournament = TournamentModel(**payload)
        new_tournament.save()
        self.tournament = new_tournament
        self.tournament_menu()

    def load_tournament(self) -> None:
        """Function to load a saved tournament"""
        saved_tournaments = {
            str(index): file
            for index, file in enumerate(TournamentModel.get_all(), 1)
        }
        saved_tournaments["q"] = "Annuler"
        user_choice = loading_screen(
            saved_tournaments, title="Tournois sauvegardés :"
        )
        if user_choice:
            tournament = TournamentModel.load_by_name(user_choice)
            if not tournament:
                raise KeyError
        else:
            return
        self.tournament = tournament
        self.tournament_menu()

    def tournament_menu(self) -> None:
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

            if self.tournament.current_round > self.tournament.round_number:
                options = load_options_to_archive()

            options.update(add_options_to_quit())

            while True:
                try:
                    user_choice = tournament_menu_screen(
                        self.tournament, options
                    )
                    if self.tournament.current_round == 0:
                        match user_choice:
                            case "1":
                                self.show_players()
                            case "2":
                                if len(self.tournament.players) == (
                                    self.tournament.round_number * 2
                                ):
                                    alert_message(
                                        message="Attention,\
vous avez atteint la limite de joueurs.",
                                        type="Error",
                                    )
                                else:
                                    contextual_controller = PlayerController()
                                    player_to_add = (
                                        contextual_controller.add_player_menu()
                                    )
                                    if (
                                        player_to_add
                                        and player_to_add.__dict__
                                        not in [
                                            player.__dict__
                                            for player in self.tournament.players
                                        ]
                                    ):
                                        self.tournament.players.append(
                                            player_to_add
                                        )
                                        self.tournament.save()
                                        self.tournament = (
                                            self.tournament.reload_data()
                                        )
                                    else:
                                        alert_message(
                                            message="Joueur déjà inscris",
                                            type="Error",
                                        )
                            case "3":
                                if len(self.tournament.players) == (
                                    self.tournament.round_number * 2
                                ):
                                    alert_message(
                                        message="Début du tournoi", type="Info"
                                    )
                                    self.tournament.current_round = 1
                                    if not self.tournament.rounds_list:
                                        self.tournament.rounds_list = []
                                    self.tournament.rounds_list.append(
                                        RoundController(
                                            tournament=self.tournament).new_round()
                                    )
                                    self.tournament.save()
                                    self.tournament_menu()

                                elif len(self.tournament.players) < (
                                    self.tournament.round_number * 2
                                ):
                                    alert_message(
                                        message="Pas assez de joueurs pour commencer",
                                        type="Error",
                                    )
                                else:
                                    alert_message(
                                        message="Le nombre de joueurs maximum est dépassé",
                                        type="Error",
                                    )
                            case "q":
                                good_bye_screen(
                                    message="Retour au menu principal"
                                )
                                break
                            case _:
                                raise KeyError
                    if self.tournament.current_round > 0:
                        # Check if the last round has been played
                        if self.tournament.current_round < self.tournament.round_number:
                            match user_choice:
                                case "1":
                                    self.show_players()
                                case "2":
                                    self.list_rounds()
                                case "3":
                                    self.tournament = RoundController(
                                        tournament=self.tournament).write_match_result()
                                    self.tournament.save()
                                    self.tournament = self.tournament.reload_data()
                                case "4":
                                    tournament = RoundController(
                                        tournament=self.tournament).end_round()
                                    self.tournament = tournament.reload_data()
                                case "q":
                                    good_bye_screen(
                                        message="Retour au menu principal"
                                    )
                                    break
                        else:
                            match user_choice:
                                case "1":
                                    self.show_players()
                                case "2":
                                    self.list_rounds()
                                case "3":
                                    self.tournament.archive()
                                    self.tournament = None
                                    good_bye_screen(
                                        message="Tournoi archivé. Retour au menu principal")
                                    break
                                case "q":
                                    good_bye_screen(
                                        message="Retour au menu principal"
                                    )
                                    break
                except KeyError:
                    alert_message(
                        message="Aucun choix ne correspond, \
    merci de sélectionner une des options du menu",
                        type="Error",
                    )
                    continue

    def show_players(self) -> None:
        """Show a list of the current tournament's players"""
        show_players_screen(
            self.tournament.get_players(),
            from_tournament=True,
        )

    def list_rounds(self) -> None:
        """Lists this tournament's rounds and their games"""
        list_rounds_screen(self.tournament.rounds_list)

    def update_player_score(
        self, nci: str, points: float
    ) -> List[PlayerModel]:
        """Makes sure the players are PlayerModel and update their scores"""
        for player in self.tournament.players:
            if not isinstance(player, PlayerModel):
                player = PlayerModel(**player)
            if player.national_chess_id == nci:
                player.update_score(points)
        return self.tournament.players


def add_options_to_quit():
    """Function to add the save/quit options to a menu"""
    return {
        "q": "Quitter",
    }


def load_options_to_manage():
    """Returns the options to manage a tournament"""
    # Options available when tournament started
    # (overwrite previous choices)

    # add option to archive
    # add option to continue to next round
    options = {
        "1": "Afficher les joueurs inscris",
        "2": "Afficher les tours",
        "3": "Inscrire les résultats d'un match",
        "4": "Passer au tour suivant (tous les matchs doivent être terminés)",
        "5": "Archiver tournoi",
    }
    return options


def load_options_to_archive():
    """Returns the options to manage a tournament"""
    # Options available when tournament started
    # (overwrite previous choices)

    # add option to archive
    # add option to continue to next round
    options = {
        "1": "Afficher les joueurs inscris",
        "2": "Afficher les tours",
        "3": "Archiver tournoi",
    }
    return options
