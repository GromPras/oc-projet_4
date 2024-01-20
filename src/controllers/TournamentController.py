from random import shuffle
from typing import List
from controllers.PlayerController import PlayerController
from models.TournamentModel import TournamentModel
from models.RoundModel import RoundModel
from models.GameModel import GameModel
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
                                    self.prepare_round()

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
                        if self.tournament.current_round < self.tournament.round_number:
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
            self.tournament.players,
            from_tournament=True,
        )

    def sort_players_for_game(self) -> None:
        """Function to sort or shuffle the players before a new round"""
        if self.tournament.current_round == 1:
            shuffle(self.tournament.players)
        else:
            self.tournament.players = sorted(
                self.tournament.players, key=lambda k: k.score,
                reverse=True
            )

    def find_new_opponent(
        self,
        player_1: PlayerModel,
        previous_games: List[List[str]],
        possible_opponents: List[PlayerModel],
    ) -> PlayerModel | None:
        """Function to check if two players already faced each other"""
        new_opponent = None
        for opponent in possible_opponents:
            if (player_1.national_chess_id, opponent.national_chess_id) not in previous_games:
                new_opponent = opponent
                return new_opponent
        return new_opponent

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
            # pair players from score, avoid similar pairs from prev matches
            for i in range(self.tournament.round_number):
                already_paired = []
                for game in games:
                    already_paired.append(game.player_1.national_chess_id)
                    already_paired.append(game.player_2.national_chess_id)

                previous_pairs = []
                for round_item in self.tournament.rounds_list:
                    [previous_pairs.append(
                        [game.player_1.national_chess_id, game.player_2.national_chess_id]) for game in round_item.games]
                players = filter(
                    lambda k: k.national_chess_id not in already_paired, self.tournament.players)

                for player in players:
                    opponents = filter(
                        lambda k: player.national_chess_id != k.national_chess_id, players)

                    player_2 = self.find_new_opponent(
                        player_1=player,
                        previous_games=previous_pairs,
                        possible_opponents=list(opponents),
                    )
                    games.append(
                        GameModel(
                            player_1=player,
                            player_1_score=0,
                            player_2=player_2,
                            player_2_score=0,
                        )
                    )
        new_round = RoundModel(
            games=games,
            name=f"Round {self.tournament.current_round}",
        )
        return new_round

    def prepare_round(self) -> None:
        """Adds a new round with players paired to the current tournament"""
        if not self.tournament.rounds_list:
            self.tournament.rounds_list = []
        self.sort_players_for_game()
        new_round = self.pair_players_for_game()
        self.tournament.rounds_list.append(new_round)
        self.tournament.save()
        self.tournament = self.tournament.reload_data()
        self.tournament_menu()

    def list_rounds(self) -> None:
        """Lists this tournament's rounds and their games"""
        list_rounds_screen(self.tournament.rounds_list)

    def write_match_result(self) -> None:
        """Function to write the result of a match"""
        current_round = self.tournament.rounds_list[
            self.tournament.current_round - 1
        ]
        if not isinstance(current_round, RoundModel):
            current_round = RoundModel(**current_round)
        games = {
            str(index): game.get_players()
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
                if not isinstance(self.tournament.players[0], PlayerModel):
                    self.tournament.players = [
                        PlayerModel(**player)
                        for player in self.tournament.players
                    ]
                match result:
                    case "1":
                        alert_message(message="Le joueur 1 gagne", type="Info")
                        game.set_score(winner="player_1")
                        [
                            player.update_score(1)
                            for player in self.tournament.players
                            if player.national_chess_id
                            == game.player_1.national_chess_id
                        ]
                        self.tournament.save()
                    case "2":
                        alert_message(message="Le joueur 2 gagne", type="Info")
                        game.set_score(winner="player_2")
                        [
                            player.update_score(1)
                            for player in self.tournament.players
                            if player.national_chess_id
                            == game.player_2.national_chess_id
                        ]
                        self.tournament.save()
                    case "3":
                        alert_message(message="Egalité", type="Info")
                        game.set_score(winner="none")
                        players_id = []
                        players_id.append(game.player_1.national_chess_id)
                        players_id.append(game.player_2.national_chess_id)
                        for player in self.tournament.players:
                            if player.national_chess_id in players_id:
                                player.update_score(0.5)
                        self.tournament.save()
                    case _:
                        break
                self.tournament = self.tournament.reload_data()
                return
            except KeyError:
                alert_message(
                    message="Aucun choix ne correspond, \
    merci de sélectionner une des options du menu",
                    type="Error",
                )
                continue

    def end_round(self) -> None:
        """Ends the current round and prepare the next"""
        current_round = self.tournament.rounds_list[
            self.tournament.current_round - 1
        ]
        if not [game.get_winner() is None for game in current_round.games]:
            alert_message(
                message="Tous les matchs ne sont pas terminés.", type="Error"
            )
        else:
            self.tournament.rounds_list[self.tournament.current_round -
                                        1] = current_round.set_round_end()
            self.tournament.current_round += 1
            if self.tournament.current_round < self.tournament.round_number:
                self.prepare_round()
                self.tournament.save()
            else:
                alert_message(message="Tournoi terminé")
            self.tournament_menu()

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
