from random import shuffle
from controllers.PlayerController import PlayerController
from models.TournamentModel import TournamentModel
from models.RoundModel import RoundModel
from models.GameModel import GameModel
from views.loading_screen import loading_screen
from views.good_bye_screen import good_bye_screen
from views.tournament_menu_screen import tournament_menu_screen
from views.show_players_screen import show_players_screen
from views.tournament_form import tournament_form
from views.list_rounds_screen import list_rounds_screen
from views.show_game_screen import show_game_screen


class TournamentController:
    """Class to handle tournament related actions"""

    def __init__(self) -> None:
        self.tournament = None

    def create_tournament(self):
        """Function to create a new tournament"""
        payload = tournament_form()
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
        saved_tournaments["q"] = "Annuler"
        while True:
            try:
                user_choice = saved_tournaments[
                    loading_screen(
                        saved_tournaments, title="Tournois sauvegardés :"
                    )
                ]
                if user_choice == "Annuler":
                    good_bye_screen(message="Retour au menu principal")
                    break
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
                                self.show_players()
                            case "2":
                                if len(self.tournament.players) == (
                                    self.tournament.round_number * 2
                                ):
                                    print(
                                        "Attention,\
vous avez atteint la limite de joueurs."
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
                                        print(self.tournament.players)
                                        self.tournament.save()
                                    else:
                                        print("Joueur déjà inscris")
                            case "3":
                                if len(self.tournament.players) == (
                                    self.tournament.round_number * 2
                                ):
                                    [
                                        player.set_score(0)
                                        for player in self.tournament.players
                                    ]
                                    print("Début du tournoi")
                                    self.tournament.current_round = 1
                                    self.prepare_round()
                                    self.tournament.save()
                                    self.tournament_menu()
                                elif len(self.tournament.players) < (
                                    self.tournament.round_number * 2
                                ):
                                    # Print error
                                    print(
                                        "Pas assez de joueurs pour commencer"
                                    )
                                else:
                                    print(
                                        "Le nombre de joueurs maximum est dépassé"
                                    )
                            case "q":
                                good_bye_screen(
                                    message="Retour au menu principal"
                                )
                                return None
                            case _:
                                raise KeyError
                    if self.tournament.current_round > 0:
                        match user_choice:
                            case "1":
                                self.show_players()
                            case "2":
                                self.list_rounds()
                            case "3":
                                self.write_match_result()
                            case "4":
                                self.end_round()
                            case "q":
                                good_bye_screen(
                                    message="Retour au menu principal"
                                )
                                break
                except KeyError:
                    print(
                        "Aucun choix ne correspond, \
    merci de sélectionner une des options du menu"
                    )
                    continue

    def show_players(self) -> None:
        """Show a list of the current tournament's players"""
        show_players_screen(
            self.tournament.players,
            from_tournament=True,
        )

    def sort_players_for_game(self) -> None:
        """Function to sort or shuffle the players before a new round"""
        if self.tournament.current_round == 1:
            shuffle(self.tournament.players)
        else:
            self.tournament.players = sorted(
                self.tournament.players, key=lambda k: k.score
            )

    def pair_players_for_game(self) -> RoundModel:
        """Creates pairs of players for the round's games"""
        games = []
        if self.tournament.current_round == 1:
            for i in range(0, len(self.tournament.players), 2):
                games.append(
                    GameModel(
                        player_1=self.tournament.players[i],
                        player_1_score=self.tournament.players[i].score,
                        player_2=self.tournament.players[i + 1],
                        player_2_score=self.tournament.players[i + 1].score,
                    )
                )
        else:
            pass
        new_round = RoundModel(
            games=games,
            name="Round 1",
        )
        return new_round

    def prepare_round(self) -> None:
        """Adds a new round with players paired to the current tournament"""
        if not self.tournament.rounds_list:
            self.tournament.rounds_list = []
        self.sort_players_for_game()
        new_round = self.pair_players_for_game()
        self.tournament.rounds_list.append(new_round)

    def list_rounds(self) -> None:
        """Lists this tournament's rounds and their games"""
        list_rounds_screen(self.tournament.rounds_list)

    def write_match_result(self) -> None:
        """Function to write the result of a match"""
        current_round = self.tournament.rounds_list[
            self.tournament.current_round - 1
        ]
        games = {
            str(index): show_game_screen(game)
            for index, game in enumerate(current_round.games, 1)
        }
        games["q"] = "Annuler"
        while True:
            try:
                user_choice = loading_screen(
                    games, title="Sélectionnez un match : "
                )
                if user_choice == "q":
                    good_bye_screen(message="Retour au menu du tournoi")
                    break
                user_choice = int(user_choice) - 1
                if not current_round.games[user_choice]:
                    raise KeyError
                game = current_round.games[user_choice]
                results = {
                    "1": game.player_1.fullname(),
                    "2": game.player_2.fullname(),
                    "3": "Egalité",
                }
                result = loading_screen(
                    results, title="Qui à gagné le match ?"
                )
                match result:
                    case "1":
                        print("Le joueur 1 gagne")
                        game.set_score(winner="player_1")
                    case "2":
                        game.set_score(winner="player_2")
                    case "3":
                        print("Egalité")
                        game.set_score(winner="none")
                    case _:
                        break
                break

            except KeyError:
                print(
                    "Aucun choix ne correspond, \
    merci de sélectionner une des options du menu"
                )
                continue

    def end_round(self) -> None:
        """Ends the current round and prepare the next"""
        self.tournament.current_round += 1
        self.prepare_round()
        self.tournament.save()
        self.tournament_menu()


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
