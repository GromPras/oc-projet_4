import os
import json
from models.PlayerModel import PlayerModel
from utils.errors import LoadError, SaveError


class GameModel:
    """Model class for the Game objects"""

    def __init__(
        self,
        round_id: str,
        player_1_id: str,
        player_2_id: str,
        player_1_score: float = 0.0,
        player_2_score: float = 0.0,
    ) -> None:
        self.round_id = round_id.split(".")[0]
        self.player_1_id = player_1_id
        self.player_2_id = player_2_id
        self.player_1_score = player_1_score
        self.player_2_score = player_2_score

    def save(self) -> None:
        """Saves the Game in the round's games list"""
        t_round = f"{self.round_id}.json"
        games = self.get_rounds_games(t_round)
        if games:
            if self.__dict__ in [game.__dict__ for game in games]:
                return
        else:
            games = []

        games.append(self)
        try:
            with open(f"data/games/{t_round}", "w", encoding="UTF-8") as json_file:
                json.dump([game.__dict__ for game in games], json_file)
        except OSError:
            raise SaveError(
                message="[ERREUR]: le fichier {file_name} n'a pas pu être sauvegardé"
            )

    @classmethod
    def get_rounds_games(cls, round_id: str):
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
                message="[ERREUR]: le fichier joueurs n'a pas pu être chargé")
