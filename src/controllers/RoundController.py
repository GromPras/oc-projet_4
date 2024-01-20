from random import shuffle
from typing import List
from models.GameModel import GameModel
from models.RoundModel import RoundModel
from models.PlayerModel import PlayerModel
from models.TournamentModel import TournamentModel
from views.alert_message import alert_message
from views.loading_screen import loading_screen


class RoundController:
    def write_match_result(
        self, tournament: TournamentModel
    ) -> TournamentModel:
        """Function to write the result of a match"""
        current_round = tournament.rounds_list[tournament.current_round - 1]
        if not isinstance(current_round, RoundModel):
            current_round = RoundModel(**current_round)
        games = {
            str(index): game.get_players()
            for index, game in enumerate(current_round.games, 1)
        }
        games["q"] = "Annuler"
        user_choice = loading_screen(
            games, title="Sélectionnez un match : ", return_raw_input=True
        )
        if user_choice:
            game_index = int(user_choice) - 1
            if not current_round.games[game_index]:
                raise KeyError
            game = current_round.games[game_index]
            print(game)
            results = {
                "1": game.player_1.fullname(),
                "2": game.player_2.fullname(),
                "3": "Egalité",
            }
            result = loading_screen(
                results, title="Qui à gagné le match ?", return_raw_input=True
            )
            if not isinstance(tournament.players[0], PlayerModel):
                tournament.players = [
                    PlayerModel(**player) for player in tournament.players
                ]
            match result:
                case "1":
                    alert_message(message="Le joueur 1 gagne", type="Info")
                    game.set_score(winner="player_1")
                    [
                        player.update_score(1)
                        for player in tournament.players
                        if player.national_chess_id
                        == game.player_1.national_chess_id
                    ]
                    tournament.save()
                    return tournament
                case "2":
                    alert_message(message="Le joueur 2 gagne", type="Info")
                    game.set_score(winner="player_2")
                    [
                        player.update_score(1)
                        for player in tournament.players
                        if player.national_chess_id
                        == game.player_2.national_chess_id
                    ]
                    tournament.save()
                    return tournament
                case "3":
                    alert_message(message="Egalité", type="Info")
                    game.set_score(winner="none")
                    players_id = []
                    players_id.append(game.player_1.national_chess_id)
                    players_id.append(game.player_2.national_chess_id)
                    for player in tournament.players:
                        if player.national_chess_id in players_id:
                            player.update_score(0.5)
                    tournament.save()
                    return tournament
                case _:
                    return

    def end_round(self, tournament: TournamentModel) -> TournamentModel:
        """Ends the current round and prepare the next"""
        current_round = tournament.rounds_list[tournament.current_round - 1]
        if not [game.get_winner() is None for game in current_round.games]:
            alert_message(
                message="Tous les matchs ne sont pas terminés.", type="Error"
            )
        else:
            tournament.rounds_list[
                tournament.current_round - 1
            ] = current_round.set_round_end()
            tournament.current_round += 1
            if tournament.current_round < tournament.round_number:
                tournament.rounds_list.append(
                    self.new_round(tournament=tournament)
                )
                tournament.save()
            else:
                alert_message(message="Tournoi terminé")
            return tournament

    def new_round(self, tournament: TournamentModel) -> RoundModel:
        """Adds a new round with players paired to the current tournament"""
        sorted_players = self.sort_players_for_game(
            current_round=tournament.current_round, players=tournament.players
        )
        new_round = self.pair_players(
            current_round=tournament.current_round,
            players=sorted_players,
            previous_rounds=tournament.rounds_list[
                : tournament.current_round - 1
            ],
            round_number=tournament.round_number,
        )
        return new_round

    def sort_players_for_game(
        self, current_round: int, players: List[PlayerModel]
    ) -> List[PlayerModel]:
        """Function to sort or shuffle the players before a new round"""
        if current_round == 1:
            shuffle(players)
            return players
        else:
            players = sorted(players, key=lambda k: k.score, reverse=True)
            return players

    def pair_players(
        self,
        current_round: int,
        players: List[PlayerModel],
        previous_rounds: List[RoundModel],
        round_number: int,
    ) -> RoundModel:
        """Creates pairs of players for a round's games"""
        games = []
        if current_round == 1:
            for i in range(0, len(players), 2):
                games.append(
                    GameModel(
                        player_1=players[i],
                        player_1_score=players[i].score,
                        player_2=players[i + 1],
                        player_2_score=players[i + 1].score,
                    )
                )
        else:
            for i in range(round_number):
                players_paired = self.get_players_already_paired(games)
                pairs_from_previous_games = (
                    self.get_pairs_from_previous_rounds(previous_rounds)
                )
                players_to_pair = filter(
                    lambda p: p.national_chess_id not in players_paired,
                    players,
                )
                for player in players_to_pair:
                    # makes sure players cannot face themselves
                    opponents = filter(
                        lambda p: player.national_chess_id
                        != p.national_chess_id,
                        players_to_pair,
                    )

                    player_2 = self.find_new_opponent(
                        player_1=player,
                        previous_pairs=pairs_from_previous_games,
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

        new_round = RoundModel(games=games, name=f"Tour {current_round}")
        return new_round

    def find_new_opponent(
        self,
        player_1: PlayerModel,
        previous_pairs: List[List[str]],
        possible_opponents: List[PlayerModel],
    ) -> PlayerModel | None:
        """Function to check if two players already faced each other"""
        new_opponent = None
        for opponent in possible_opponents:
            if (
                player_1.national_chess_id,
                opponent.national_chess_id,
            ) not in previous_pairs:
                new_opponent = opponent
                return new_opponent
        return new_opponent

    def get_players_already_paired(self, games: List[GameModel]) -> List:
        players_in_games = []
        for game in games:
            players_in_games.append(game.player_1.national_chess_id)
            players_in_games.append(game.player_2.national_chess_id)
        return players_in_games

    def get_pairs_from_previous_rounds(
        self, previous_rounds: List[RoundModel]
    ) -> List:
        previous_pairs = []
        for p_round in previous_rounds:
            [
                previous_pairs.append(
                    [
                        game.player_1.national_chess_id,
                        game.player_2.national_chess_id,
                    ]
                )
                for game in p_round.games
            ]
        return previous_pairs
