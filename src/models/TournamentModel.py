from __future__ import annotations
import os
import json
from typing import List
from models.PlayerModel import PlayerModel
from models.RoundModel import RoundModel
from utils.errors import OperationError


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
        self.rounds_list = (
            [RoundModel(**item) for item in rounds_list]
            if len(rounds_list) > 0
            else []
        )
        self.players = (
            [PlayerModel(**player) for player in players]
            if len(players) > 0
            else []
        )
        self.current_round = current_round

    def save(self, archive=False) -> TournamentModel | None:
        """Saves a tournament object to a json file"""
        self_dictionnary = self.__dict__
        if len(self.players) > 0 and isinstance(self.players[0], PlayerModel):
            self_dictionnary["players"] = [
                player.__dict__ for player in self.players
            ]
        else:
            self_dictionnary["players"] = self.players
        if len(self.rounds_list) > 0:
            if isinstance(self.rounds_list[0], RoundModel):
                self_dictionnary["rounds_list"] = [
                    game_round.to_dict() for game_round in self.rounds_list
                ]
        try:
            path = "data/archived/" if archive else "data/tournaments/"
            with open(
                f"{path}{self.starts}_tournoi_{self.name}.json",
                mode="w",
                encoding="UTF-8",
            ) as json_file:
                json.dump(self_dictionnary, json_file)
            print("Tournoi sauvegardé")
            return self
        except OSError:
            print("[ERREUR]: le fichier n'a pas pu être sauvegardé")

    def reload_data(self) -> TournamentModel:
        tournament_data = None
        with open(
            f"data/tournaments/{self.starts}_tournoi_{self.name}.json", "r"
        ) as json_file:
            tournament_data = json.load(json_file)
        tournament = TournamentModel(**tournament_data)
        return tournament

    def archive(self) -> TournamentModel | None:
        """Function to mark the current tournament as archived"""
        if self.save(archive=True) is not None:
            try:
                os.remove(
                    f"data/tournaments/{self.starts}_tournoi_{self.name}.json")
            except OSError:
                raise OperationError(
                    message="Le tournoi n'a pas pu être supprimé")

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
        return tournament

    def __repr__(self) -> str:
        """Simple representation of a tournament"""
        return f"{self.name} - {self.location} - Du {self.starts} au \
{self.ends} - {self.round_number} rounds - \
Tour: {self.current_round}"
