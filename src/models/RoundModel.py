from typing import List, Optional
from datetime import datetime
from models.GameModel import GameModel


class RoundModel:
    """Model class for the round objects"""

    def __init__(
        self,
        name: str,
        games: List = [],
        started_on: Optional[str] = None,
        ended_on: Optional[str] = None,
    ) -> None:
        self.games = (
            [GameModel.loads(game) for game in games] if len(games) > 0 else []
        )
        self.name = name
        self.started_on = started_on if started_on else datetime.now()
        self.ended_on = ended_on

    def to_dict(self):
        """Returns an instance of Round as a dictionnary"""
        return {
            "games": [game.as_tuple() for game in self.games],
            "name": self.name,
            "started_on": str(self.started_on),
            "ended_on": str(self.ended_on),
        }
