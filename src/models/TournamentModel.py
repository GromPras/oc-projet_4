from __future__ import annotations
import os
import json
from typing import List
from models.PlayerModel import PlayerModel


class TournamentModel:
    """Model class for the Tournament objects"""

    def __init__(
        self,
        name: str,
        location: str,
        starts: str,
        ends: str,
        round_number: int = 0,
        description: str = "",
        current_round: int = 0,
        players: List = [],
        rounds_list: List = [],
    ):
        self.name = name
        self.location = location
        self.starts = starts
        self.ends = ends
        self.round_number = round_number
        self.description = description
        self.rounds_list = rounds_list
        self.players = players
        self.current_round = current_round

    def save(self) -> TournamentModel | None:
        """Saves a tournament object to a json file"""
        self_dictionnary = self.__dict__
        self_dictionnary["players"] = [
            player.__dict__ for player in self.players
        ]
        try:
            with open(
                f"data/tournaments/{self.starts}_tournoi_{self.name}.json",
                mode="w",
                encoding="UTF-8",
            ) as json_file:
                json.dump(self_dictionnary, json_file)
            print("Tournoi sauvegardé")
            return self
        except OSError:
            print("[ERREUR]: le fichier n'a pas pu être sauvegardé")

    @classmethod
    def get_all(cls) -> List[str]:
        """Returns all saved tournaments in data folder"""
        tournaments = os.listdir("data/tournaments")
        tournaments = sorted(tournaments, reverse=True)
        return tournaments

    @classmethod
    def load_by_name(cls, name: str) -> TournamentModel:
        """Loads a specific tournament from a json file"""
        tournament_data = None
        with open(f"data/tournaments/{name}", "r") as json_file:
            tournament_data = json.load(json_file)

        tournament = cls(**tournament_data)
        if len(tournament.players) > 0:
            tournament.players = [
                PlayerModel(**player) for player in tournament.players
            ]
        return tournament

    def __repr__(self) -> str:
        """Simple representation of a tournament"""
        return f"{self.name} - {self.location} - Du {self.starts} au \
{self.ends} - {self.round_number} rounds - \
{self.description if not None else ''}"
