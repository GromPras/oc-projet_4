from __future__ import annotations
import json
from typing import Optional
from utils.errors import SaveError, LoadError


class PlayerModel:
    """Class model for the Player objects"""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: str,
        national_chess_id: str,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.national_chess_id = national_chess_id

    def __repr__(self) -> str:
        return f"{self.national_chess_id} - \
{self.fullname()} - né(e) le : {self.birth_date}"

    def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def save(self) -> PlayerModel:
        """Saves a Player object to a global players json file"""
        players = self.get_all()
        if players:
            if self.__dict__ in [player.__dict__ for player in players]:
                return self
        else:
            players = []

        # Removes score attribute before saving player
        delattr(self, "score")
        players.append(self)
        try:
            with open("data/players.json", "w", encoding="UTF-8") as json_file:
                json.dump([player.__dict__ for player in players], json_file)

            return self
        except OSError:
            raise SaveError(
                message="[ERREUR]: le fichier n'a pas pu être sauvegardé"
            )

    def update_score(self, value: float) -> None:
        try:
            self.score += float(value)
        except ValueError:
            raise SaveError(
                message="Le score doit être un nombre, aucune modification n'a été effectuée"
            )

    @classmethod
    def get_all(cls):
        """Retrieve the players from a json file"""
        players_data = []
        try:
            with open("data/players/players.json", "r") as json_file:
                players_data = json.load(json_file)

            if players_data:
                players = [cls(**player) for player in players_data]
                return players
        except OSError:
            raise LoadError(
                message="[ERREUR]: le fichier joueurs n'a pas pu être chargé"
            )

    @classmethod
    def load_by_id(cls, id: str) -> PlayerModel | None:
        """Takes the nid of a player or its __repr__ to load a Player object
        Returns None if no player could be loaded"""
        national_chess_id = id.split(" ")[0]
        players = cls.get_all()
        if players and national_chess_id:
            player_data = [
                player
                for player in players
                if player.national_chess_id == national_chess_id
            ]
            return player_data[0] if len(player_data) > 0 else None
