from datetime import datetime
from typing import List, Dict
from models.PlayerModel import PlayerModel
from models.RoundModel import RoundModel
from utils.functions import clear_screen


class RoundViews:
    def show_rounds(self, rounds: List[Dict[RoundModel, List[Dict[PlayerModel, float]]]]) -> None:
        clear_screen()
        for index, r in enumerate(rounds, 1):
            print(f"""
{r['round'].name} \
Début: {r['round'].started_on.split('.')[0]} - Fin: {r['round'].ended_on.split('.')[0] if not "None" else "En cours"}""")
            print("-"*40)
            for g in r["games"]:
                print(f"""
{g["player_1"].fullname()} (score: {g["player_1_score"]}) \
contre {g["player_2"].fullname()} (score: {g["player_2_score"]})""")
            if index < len(rounds):
                print("-"*40)
        
        print("_"*80)