from typing import Dict


class GameViews:
    def game_winner(self, game: Dict) -> str:
        print(f"""
{game["player_1"].fullname()} contre {game["player_2"].fullname()}""")
        print("_"*40)
        print(f"1: {game['player_1'].fullname()} gagne")
        print(f"2: {game['player_2'].fullname()} gagne")
        print("3: Egalité")
        while True:
            result = input("Quel est le résultat ?")
            match result:
                case "1":
                    return game["player_1"].national_chess_id
                case "2":
                    return game["player_2"].national_chess_id
                case "3":
                    return "none"
                case "q":
                    return None
                case _:
                    print("Aucun choix ne correspond, réessayez")
                    continue