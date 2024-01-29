from __future__ import annotations
import json
import os
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

        players.append(self)
        try:
            with open(
                "data/players/players.json", "w", encoding="UTF-8"
            ) as json_file:
                json.dump([player.__dict__ for player in players], json_file)

            return self
        except OSError:
            raise SaveError(
                message="[ERREUR]: le fichier n'a pas pu être sauvegardé"
            )

    def save_in_tournament(self, tournament_id: str):
        full_path = f'data/tournament_players/{tournament_id}'
        new_tournament_player = {
            "player_id": self.national_chess_id,
            "player_score": 0,
        }
        tournament_players = self.get_tournament_players(
            tournament_id=tournament_id, raw_data=True)
        if tournament_players:
            if new_tournament_player in tournament_players:
                return
        else:
            tournament_players = []
        tournament_players.append(new_tournament_player)
        try:
            with open(full_path, "w", encoding="UTF-8") as json_file:
                json.dump(tournament_players, json_file)
        except OSError:
            raise SaveError(
                message="[ERREUR]: le fichier n'a pas pu être sauvegardé"
            )
    
    def update_score(self, tournament_id: str, value: float) -> None:
        t_players = self.get_tournament_players(tournament_id=tournament_id, raw_data=True)
        for p in t_players:
            if p["player_id"] == self.national_chess_id:
                p["player_score"] += value
        try:
            full_path = f'data/tournament_players/{tournament_id}'
            with open(full_path, "w", encoding="UTF-8") as json_file:
                json.dump(t_players, json_file)
        except OSError:
            raise SaveError(
                message="[ERREUR]: le fichier n'a pas pu être sauvegardé"
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
        players = cls.get_all()
        if players and id:
            player_data = [
                player
                for player in players
                if player.national_chess_id == id
            ]
            return player_data[0] if len(player_data) > 0 else None

    @classmethod
    def get_tournament_players(cls, tournament_id: str, raw_data=False):
        data = []
        tournament_players = []
        try:
            with open(f"data/tournament_players/{tournament_id}") as json_file:
                data = json.load(json_file)

            if raw_data:
                return data

            for line_item in data:
                tournament_players.append(
                    {
                        "player": PlayerModel.load_by_id(
                            line_item["player_id"]
                        ),
                        "player_score": line_item["player_score"]
                    }
                )

            return tournament_players

        except OSError:
            raise LoadError(
                message="[ERREUR]: le fichier joueurs n'a pas pu être chargé"
            )

    @classmethod
    def remove_tournament_players(cls, tournament_id: str) -> None:
        try:
            os.remove(f"data/tournament_players/{tournament_id}")
        except OSError:
            print(f"Error deleting {tournament_id} players file")