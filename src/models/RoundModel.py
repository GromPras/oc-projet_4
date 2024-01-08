from typing import List, Tuple, Optional
from datetime import datetime


class RoundModel:
    def __init__(
        self,
        games: List[Tuple],
        name: str,
        started_on: Optional[str] = None,
        ended_on: Optional[str] = None,
    ) -> None:
        self.games = games
        self.name = name
        self.started_on = started_on if started_on else datetime.now()
        self.ended_on = ended_on

    def to_dict(self):
        return {
            "games": [
                (
                    [game[0][0].__dict__, game[0][1]],
                    [game[1][0].__dict__, game[1][1]],
                )
                for game in self.games
            ],
            "name": self.name,
            "started_on": str(self.started_on),
            "ended_on": str(self.ended_on),
        }
