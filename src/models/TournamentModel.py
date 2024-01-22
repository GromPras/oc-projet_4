from __future__ import annotations
import os
import json
from typing import List, Optional
from utils.functions import generate_id
from utils.errors import SaveError, OperationError


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
        return f"{self.name} - {self.location} - \
Du {self.starts} au {self.ends} \
Joué en {self.number_of_rounds} tours - Tour actuel: {self.current_round}"

    def save(self, archive=False) -> None:
        """Saves a Tournament to a json file
        If archive is True, the file is saved in the /archived directory
        """
        self_dict = self.__dict__
        file_name = f"{self.id}.json"
        try:
            with open(
                f"data/{'archives/' if archive else 'tournaments/'}{file_name}",
                mode="w",
                encoding="UTF-8",
            ) as json_file:
                json.dump(self_dict, json_file)
        except OSError:
            raise SaveError(
                message="[ERREUR]: le fichier {file_name} n'a pas pu être sauvegardé"
            )

    def archive(self) -> TournamentModel:
        if self.save(archive=True) is not None:
            try:
                os.remove(
                    f"data/tournaments/{self.starts}_tournoi_{self.name}.json"
                )
            except OSError:
                raise OperationError(
                    message="[ERREUR]: Le tournoi n'a pas pu être archivé"
                )

    def get_id(self) -> str:
        return f"{self.id}.json"
    # def to_dict(self) -> None:
    #     self_dict = self.__dict__
    #     if len(self.players > 0):
    #         self_dict["players"] = [player.__dict__ for player in self.players]
    #     if len(self.rounds_list) > 0:
    #         self_dict["rounds_list"] = [
    #             game_round.to_dict() for game_round in self.rounds_list
    #         ]

    @classmethod
    def get_all(cls) -> List[TournamentModel]:
        """Returns all tournaments files in data/tournaments/ folder"""
        tournaments = os.listdir("data/tournaments")
        tournaments = sorted(tournaments, reverse=True)
        tournaments = [cls.load_by_id(tournament)
                       for tournament in tournaments]
        return tournaments

    @classmethod
    def load_by_id(cls, id: str) -> TournamentModel:
        tournament_data = None
        with open(f"data/tournaments/{id}", "r") as json_file:
            tournament_data = json.load(json_file)

        tournament = cls(**tournament_data)
        return tournament
