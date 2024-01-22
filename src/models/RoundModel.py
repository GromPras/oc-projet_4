from __future__ import annotations
from datetime import datetime
from random import shuffle
from typing import List, Optional, Dict
from models.GameModel import GameModel
from models.PlayerModel import PlayerModel


class RoundModel:
    """Model class for Round objects"""

    def __init__(self, name: str, games: List = [], started_on: Optional[str] = None, ended_on: Optional[str] = None) -> None:
        self.name = name,
        self.games = (
            [GameModel(**game) for game in games] if len(games) > 0 else []
        )
        self.started_on = started_on if started_on else datetime.now()
        self.ended_on = ended_on

    def to_dict(self) -> Dict[str, str]:
        """Returns an instance of Round as a dictionnary"""
        self_dict = self.__dict__
        self_dict["games"] = [game.__dict__ for game in self.games]
        return self_dict

    def new_round(self, round_number: int, players: List[PlayerModel], previous_rounds: List[RoundModel]) -> RoundModel:
        sorted_players = self.sort_players_for_game(
            round_number=round_number, players=players)
        return self.pair_players(round_number=round_number, players=sorted_players, previous_rounds=previous_rounds)

    def set_round_end(self) -> RoundModel:
        self.ended_on = datetime.now()
        return self

    def sort_players_for_game(self, round_number: int, players: List[PlayerModel]) -> List[PlayerModel]:
        """Function to sort or shuffle the players before a new round"""
        if round_number == 1:
            shuffle(players)
            return players
        else:
            players = sorted(
                players, key=lambda p: p.score,
                reverse=True
            )
            return players

    def pair_players(self, round_number: int, players: List[PlayerModel], previous_rounds: List[RoundModel]) -> RoundModel:
        """Creates pairs of players for a round's games"""
        games = []
        if round_number == 1:
            for i in range(0, len(players), 2):
                games.append(
                    GameModel(
                        player_1=players[i],
                        player_1_score=players[i].socre,
                        player_2=players[i + 1],
                        player_2_score=players[i + 1].score
                    )
                )
        else:
            players_paired = self.get_players_already_paired(games)
            pairs_from_previous_games = self.get_pairs_from_previous_rounds(
                previous_rounds)
            players_to_pair = filter(
                lambda p: p.national_chess_id not in players_paired, players
            )
            for player in players_to_pair:
                # makes sure players cannot face themselves
                opponents = filter(
                    lambda p: player.national_chess_id != p.national_chess_id, players
                )

                player_2 = self.find_new_opponent(
                    player_1=player,
                    previous_pairs=pairs_from_previous_games,
                    possible_opponents=list(opponents)
                )

                games.append(
                    GameModel(
                        player_1=player,
                        player_1_score=0,
                        player_2=player_2,
                        player_2_score=0
                    )
                )

        new_round = RoundModel(
            games=games,
            name=f"Tour {round_number}"
        )
        return new_round

    def get_players_already_paired(self, games: List[RoundModel]) -> List:
        players_in_games = []
        for game in games:
            players_in_games.append(game.player_1.national_chess_id)
            players_in_games.append(game.player_2.national_chess_id)
        return players_in_games

    def get_pairs_from_previous_rounds(self, previous_rounds: List[RoundModel]) -> List:
        previous_pairs = []
        for p_round in previous_rounds:
            [previous_pairs.append(
                [
                    game.player_1.national_chess_id,
                    game.player_2.national_chess_id
                ]) for game in p_round.games
             ]
        return previous_pairs

    def find_new_opponent(self, player_1: PlayerModel, previous_pairs: List[List[str]], possible_opponents: List[PlayerModel]) -> PlayerModel | None:
        """Returns an oponent the player has not yet faced in a game"""
        for opponent in possible_opponents:
            if (player_1.national_chess_id, opponent.national_chess_id) not in previous_pairs:
                return opponent
        return None
