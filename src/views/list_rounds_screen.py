from typing import List
from models.RoundModel import RoundModel


def list_rounds_screen(rounds: List[RoundModel]) -> None:
    for item in rounds:
        print(f"Match du {item.name}")
        [
            print(
                f"{game[0][0]['first_name']} {game[0][0]['last_name']} \
contre {game[1][0]['first_name']} {game[1][0]['last_name']}"
            )
            for game in item.games
        ]
