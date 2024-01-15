from __future__ import annotations
import json


class PlayerModel:
    """Model class for the Player objects"""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: str,
        national_chess_id: str,
        score: int = 0,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.national_chess_id = national_chess_id
        self.score = score

    def __repr__(self) -> str:
        """Simple representation of a player"""
        return f"#{self.national_chess_id} - \
{self.last_name} {self.first_name} - né(e) le : {self.birth_date}"

    def fullname(self) -> str:
        """Returns the full name of the player"""
        return f"{self.first_name} {self.last_name}"

    def save(self) -> PlayerModel | None:
        """Saves a player object to a global players json file"""
        players = self.get_all()
        if players:
            if self.__dict__ in [player.__dict__ for player in players]:
                print("Joueur déjà enregistré")
                return self
        else:
            players = []
        delattr(self, "score")
        players.append(self)
        try:
            with open("data/players.json", "w", encoding="UTF-8") as json_file:
                json.dump([player.__dict__ for player in players], json_file)

            print("Joueur sauvegardé")
            return self
        except OSError:
            print("[ERREUR]: le fichier n'a pas pu être sauvegardé")

    def update_score(self, value: float) -> None:
        """Adds value to the player's score"""
        try:
            float(value)
            self.score += float(value)
        except ValueError:
            print("Le score doit être un nombre")
            print("Le score n'a pas été modifié")

    @classmethod
    def get_all(cls):
        """Retrieve the players from a json file"""
        players_data = None
        try:
            with open("data/players.json", "r") as json_file:
                players_data = json.load(json_file)

            if players_data:
                players = [cls(**player) for player in players_data]

                return players
        except OSError:
            print("[ERREUR]: le fichier joueurs n'a pas pu être chargé")

    @classmethod
    def load_by_id(cls, id: str) -> PlayerModel | None:
        """Takes the string __repr__ of a player to load a player object"""
        national_chess_id = id.split(" ")[0][1:]
        players = cls.get_all()
        if players and national_chess_id:
            data = [
                player
                for player in players
                if player.national_chess_id == national_chess_id
            ]
            return data[0] if len(data) > 0 else None
