from __future__ import annotations
import os
import json
from datetime import datetime
from typing import List, Optional
from utils.functions import generate_id
from utils.errors import SaveError


class RoundModel:
    """Model class for Round objects"""

    def __init__(
        self,
        tournament_id: str,
        name: str,
        round_id: Optional[str] = None,
        started_on: Optional[str] = None,
        ended_on: Optional[str] = None,
    ) -> None:
        if round_id:
            self.round_id = round_id.split(".")[0]
        else:
            self.round_id = generate_id(type="ROUND")
        self.tournament_id = tournament_id.split(".")[0]
        self.name = name
        self.started_on = started_on if started_on else datetime.now()
        self.ended_on = ended_on

    def save(self) -> None:
        """Saves the current round in the Db"""
        self_dict = {
            "round_id": self.round_id.split(".")[0],
            "tournament_id": self.tournament_id,
            "name": self.name,
            "started_on": str(self.started_on),
            "ended_on": str(self.ended_on),
        }
        file_name = f"{self.round_id}.json"
        try:
            with open(
                f"data/rounds/{file_name}", mode="w", encoding="UTF-8"
            ) as json_file:
                json.dump(self_dict, json_file)
        except OSError:
            raise SaveError(
                message="[ERREUR]: le fichier {file_name} n'a pas pu être sauvegardé"
            )

    def get_id(self) -> str:
        """Returns the round's db file name"""
        return f"{self.round_id}.json"

    def remove(self) -> None:
        """Removes the round from db"""
        try:
            os.remove(f"data/rounds/{self.get_id()}")
        except OSError:
            print(f"Error deleting {self.round_id} round file")

    def set_round_end(self) -> RoundModel:
        self.ended_on = datetime.now()
        return self

    @classmethod
    def load_by_id(cls, round_id: str) -> RoundModel:
        """Returns a round object from an id"""
        round_data = None
        if not os.path.exists(f"data/games/{round_id}"):
            return
        with open(f"data/rounds/{round_id}", "r") as json_file:
            round_data = json.load(json_file)

        t_round = cls(**round_data)
        return t_round

    @classmethod
    def get_tournament_rounds(cls, tournament_id: str) -> List[RoundModel]:
        """Returns the given tournament's rounds"""
        files = os.listdir("data/rounds")
        rounds = [cls.load_by_id(round_id=f) for f in files]
        t_rounds = filter(
            lambda r: r.tournament_id == tournament_id.split(".")[0], rounds
        )
        return sorted(list(t_rounds), key=lambda r: r.name)
