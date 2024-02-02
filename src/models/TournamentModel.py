from __future__ import annotations
import os
import json
from typing import List, Dict
from utils.functions import generate_id
from utils.errors import SaveError, LoadError


class TournamentModel:
    """Model class for the Tournament objects"""

    def __init__(
        self,
        name: str,
        location: str,
        starts: str,
        ends: str,
        id: str = "",
        number_of_rounds: int = 4,
        description: str = "",
        current_round: int = 0,
    ) -> None:
        self.id = id if id != "" else generate_id(type="TOURNAMENT")
        self.name = name
        self.location = location
        self.starts = starts
        self.ends = ends
        self.number_of_rounds = number_of_rounds
        self.description = description
        self.current_round = current_round

    def __repr__(self) -> str:
        """Custom representation of the object"""
        return f"{self.name} - {self.location} - \
Du {self.starts} au {self.ends} \
Joué en {self.number_of_rounds} tours - Tour actuel: {self.current_round}"

    def save(self) -> None:
        """Saves a Tournament to a json file"""
        self_dict = self.__dict__
        file_name = f"{self.id}.json"
        try:
            with open(
                f"data/tournaments/{file_name}",
                mode="w",
                encoding="UTF-8",
            ) as json_file:
                json.dump(self_dict, json_file)
        except OSError:
            raise SaveError(
                message="[ERREUR]: le fichier {file_name} n'a pas pu être sauvegardé"
            )

    def remove(self) -> None:
        """Remove the tournament from db"""
        try:
            os.remove(f"data/tournaments/{self.get_id()}")
        except OSError:
            print(f"Error deleting {self.id} tournament file")

    def get_id(self) -> str:
        """Return the tournament db file name"""
        return f"{self.id}.json"

    def add_round(self) -> None:
        """Setter for the current round number"""
        self.current_round += 1

    @classmethod
    def get_all(cls) -> List[TournamentModel]:
        """Returns all tournaments files in data/tournaments/ folder"""
        tournaments = os.listdir("data/tournaments")
        tournaments = sorted(tournaments, reverse=True)
        tournaments = [
            cls.load_by_id(tournament) for tournament in tournaments
        ]
        return tournaments

    @classmethod
    def load_by_id(cls, id: str) -> TournamentModel:
        """Return a tournament from an id"""
        tournament_data = None
        with open(f"data/tournaments/{id}", "r") as json_file:
            tournament_data = json.load(json_file)

        tournament = cls(**tournament_data)
        return tournament

    @classmethod
    def get_archives(cls) -> List[str]:
        """Return the archived tournaments list"""
        archives = os.listdir("data/archives")
        archives = sorted(archives)
        return archives

    @classmethod
    def load_archive_by_name(cls, file_name: str) -> Dict:
        """Load and return an archived tournament's data"""
        data = None
        try:
            with open(f"data/archives/{file_name}", "r") as json_file:
                data = json.load(json_file)
            return data
        except OSError:
            raise LoadError(message="Error loading archive")
