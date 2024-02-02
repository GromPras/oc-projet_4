from typing import List, Dict
from models.PlayerModel import PlayerModel
from models.RoundModel import RoundModel
from utils.functions import clear_screen


class RoundViews:
    def show_rounds(
        self, rounds: List[Dict[RoundModel, List[Dict[PlayerModel, float]]]]
    ) -> None:
        clear_screen()
        print("Légende: V = Victoire, D = Défaite, E = Egalité")
        print(
            "Si les deux joueurs affichent (D)\
cela veut dire que le match n'est pas encore fini."
        )
        print()
        for index, r in enumerate(rounds, 1):
            start = r["round"].started_on.split(".")[0]
            end = "En cours"
            if r["round"].ended_on != "None":
                end = r["round"].ended_on.split(".")[0]
            print(f"""{r['round'].name} Début: {start} - Fin: {end}""")
            print("-" * 40)
            for g in r["games"]:
                print(g.round_infos())
            if index < len(rounds):
                print("-" * 40)

        print("_" * 80)
