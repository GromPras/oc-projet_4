from __future__ import annotations
from typing import Tuple, Dict
from models.PlayerModel import PlayerModel


class GameModel:
    """Model class for the game objects"""

    def __init__(
        self,
        player_1: Dict,
        player_2: Dict,
        player_1_score: float = 0,
        player_2_score: float = 0,
    ) -> None:
        self.player_1 = PlayerModel(**player_1)
        self.player_1_score = player_1_score
        self.player_2 = PlayerModel(**player_2)
        self.player_2_score = player_2_score

    def __repr__(self) -> str:
        return f"Joueur 1 : {self.player_1.fullname()} - {self.player_1_score}\
Joueur 2 : {self.player_2.fullname()} - {self.player_2_score}"

    def as_tuple(self) -> Tuple:
        """Returns an instance of Game as a tuple"""
        return (
            [self.player_1.__dict__, self.player_1_score],
            [self.player_2.__dict__, self.player_2_score],
        )

    def set_score(self, winner: str) -> None:
        match winner:
            case "player_1":
                self.player_1_score = 1
                self.player_1.update_score(1)
            case "player_2":
                self.player_2_score = 1
                self.player_2.update_score(1)
            case "none":
                self.player_1.update_score(0.5)
                self.player_2.update_score(0.5)
                self.player_1_score = 0.5
                self.player_2_score = 0.5

    @classmethod
    def loads(cls, game: Tuple) -> GameModel:
        """Functions to construct an object from a game Tuple"""
        return GameModel(
            player_1=game[0][0],
            player_1_score=game[0][1],
            player_2=game[1][0],
            player_2_score=game[1][1],
        )
