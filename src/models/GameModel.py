from __future__ import annotations
import os
import json
from typing import Optional, Dict, Any, Self
from models.PlayerModel import PlayerModel
from utils.errors import LoadError, SaveError
from utils.functions import score_to_letter


class GameModel:
    """Model class for the Game objects"""

    def __init__(
        self,
        round_id: str,
        player_1_id: str,
        player_2_id: str,
        player_1_score: float = 0.0,
        player_2_score: float = 0.0,
        game_id: Optional[str] = None,
    ) -> None:
        self.round_id = round_id.split(".")[0]
        self.player_1_id = player_1_id
        self.player_2_id = player_2_id
        self.player_1_score = player_1_score
        self.player_2_score = player_2_score
        self.game_id = game_id

    def __repr__(self) -> str:
        """Custom representation of the object"""
        g = self.game_infos()
        return f"""{g["player_1"].fullname()} (score: {g["player_1_score"]}) \
contre {g["player_2"].fullname()} (score: {g["player_2_score"]})"""

    def to_dict(self) -> Dict:
        """Returns a dictionnary to save in the db"""
        g = self.game_infos()
        return {
            "player_1": g["player_1"].fullname(),
            "player_1_score": g["player_1_score"],
            "player_2": g["player_2"].fullname(),
            "player_2_score": g["player_2_score"],
        }

    def save(self) -> None:
        """Saves the Game in the round's games list in the db"""
        t_round = f"{self.round_id}.json"
        games = self.get_rounds_games(t_round)
        if games:
            self.game_id = len(games) + 1
            if self.__dict__ in [game.__dict__ for game in games]:
                return
        else:
            games = []
            self.game_id = 1

        games.append(self)
        try:
            with open(
                f"data/games/{t_round}", "w", encoding="UTF-8"
            ) as json_file:
                json.dump([game.__dict__ for game in games], json_file)
        except OSError:
            raise SaveError(
                message="[ERREUR]: le fichier {file_name} n'a pas pu être sauvegardé"
            )

    def update(self) -> None:
        """Update the Game in the round's games list"""
        t_round = f"{self.round_id}.json"
        games = self.get_rounds_games(t_round)
        if games:
            for game in games:
                if self.game_id == game.game_id:
                    game.player_1_score = self.player_1_score
                    game.player_2_score = self.player_2_score
        else:
            raise SaveError(
                message="[ERREUR]: le match n'a pas pu être mis à jour"
            )

        try:
            with open(
                f"data/games/{t_round}", "w", encoding="UTF-8"
            ) as json_file:
                json.dump([game.__dict__ for game in games], json_file)
        except OSError:
            raise SaveError(
                message="[ERREUR]: le fichier {file_name} n'a pas pu être sauvegardé"
            )

    def game_infos(self) -> Dict[str, Any]:
        """Loads the players informations based on their ids"""
        player_1 = PlayerModel.load_by_id(self.player_1_id)
        player_2 = PlayerModel.load_by_id(self.player_2_id)
        if player_1 and player_2:
            game = {
                "player_1": player_1,
                "player_1_score": self.player_1_score,
                "player_2": player_2,
                "player_2_score": self.player_2_score,
            }
            return game

    def round_infos(self) -> str:
        g = self.game_infos()
        return f"""\
{g["player_1"].fullname()} (score: {score_to_letter(g["player_1_score"])}) \
contre {g["player_2"].fullname()} (score: {score_to_letter(g["player_2_score"])})"""

    def set_player_score(self, player: str, score: float) -> Self:
        """Setter for the player's score"""
        if player == self.player_1_id:
            self.player_1_score = score
        elif player == self.player_2_id:
            self.player_2_score = score
        return self

    @classmethod
    def get_rounds_games(cls, round_id: str):
        """Retrieves the given round's games"""
        games_data = []
        if not os.path.exists(f"data/games/{round_id}"):
            return
        try:
            with open(f"data/games/{round_id}", "r") as json_file:
                games_data = json.load(json_file)
            if games_data:
                games = [cls(**game) for game in games_data]
                return games
            return None
        except OSError:
            raise LoadError(
                message="[ERREUR]: le fichier joueurs n'a pas pu être chargé"
            )

    @classmethod
    def remove(cls, round_id: str) -> None:
        """Removes the round's games from the db"""
        try:
            os.remove(f"data/games/{round_id}")
        except OSError:
            print(f"Error deleting {round_id} games files")
