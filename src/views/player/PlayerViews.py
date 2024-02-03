from typing import List, Dict
from models.PlayerModel import PlayerModel
from utils.functions import clear_screen, spacer
from utils import validation


class PlayerViews:

    def index(self, players: List[PlayerModel]) -> None:
        """Displays all the players"""
        clear_screen()
        print("Liste des joueurs")
        print("_" * 80)
        sorted_players = sorted(players, key=lambda p: p.last_name)
        [self.show(player) for player in sorted_players]

    def show(self, player: PlayerModel) -> None:
        """Displays a player"""
        print(player)

    def leaderboard(self, players: List[Dict]) -> None:
        sort_by_score = sorted(
            players, key=lambda s: s["player_score"], reverse=True
        )
        print("Score|     NID| Nom")
        for contender in sort_by_score:
            print(
                f"""{spacer(length=5-len(str(contender['player_score'])))}\
{contender['player_score']}| \
{contender['player'].national_chess_id}| \
{contender["player"].fullname()}"""
            )

    def player_form(self) -> Dict[str, str]:
        clear_screen()
        new_player = {}

        fields_requirements = {
            "first_name": {
                "prompt": "Prénom : ",
                "validation_func": lambda v: validation.field_length(
                    v, 2
                ).title(),
            },
            "last_name": {
                "prompt": "Nom : ",
                "validation_func": lambda v: validation.field_length(
                    v, 2
                ).title(),
            },
            "birth_date": {
                "prompt": "Date de naissance (format: jjmmaaaa) : ",
                "validation_func": lambda v: validation.field_date(v),
            },
            "national_chess_id": {
                "prompt": "Identifiant national d'échecs (format: AA00000) : ",
                "validation_func": lambda v: validation.national_chess_id(v),
            },
        }

        for field, requirements in fields_requirements.items():
            new_player[field] = validation.validate_input(
                requirements["prompt"], requirements["validation_func"]
            )

        return new_player
