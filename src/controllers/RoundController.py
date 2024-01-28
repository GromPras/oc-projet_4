from random import shuffle
from typing import List, Dict
from models.GameModel import GameModel
from models.PlayerModel import PlayerModel
from models.RoundModel import RoundModel
from models.TournamentModel import TournamentModel
from utils.errors import SaveError
from views.round.RoundViews import RoundViews
from views.shared.alert_message import alert_message


class RoundController:
    def new(self, tournament_id: str, round_number: int):
        tournament = TournamentModel.load_by_id(id=tournament_id)
        players = PlayerModel.get_tournament_players(
            tournament_id=tournament.get_id(), raw_data=True)
        next_round = int(round_number)
        sorted_players = self.sort_players_for_next_round(players, next_round)
        new_round = RoundModel(
            tournament_id=tournament.get_id().split(".")[0],
            name=f"Round {next_round}"
        )
        try:
            round_games = self.generate_pairs(
                round_id=new_round.get_id(),
                round_number=next_round,
                number_of_pairs=tournament.number_of_rounds,
                players=sorted_players
            )
            [game.save() for game in round_games]
            new_round.save()
        except SaveError as e:
            alert_message(message=str(e), type="Info")

    def generate_pairs(
        self,
        round_id: str,
        round_number: int,
        number_of_pairs: int,
        players: List[Dict]
    ) -> List[GameModel]:
        pairs = []
        if round_number == 1:
            for i in range(0, len(players), 2):
                pairs.append(GameModel(
                    round_id,
                    player_1_id=players[i]["player_id"],
                    player_1_score=players[i]["player_score"],
                    player_2_id=players[i + 1]["player_id"],
                    player_2_score=players[i + 1]["player_score"]
                ))
            return pairs
        else:
            for p in range(number_of_pairs):
                pass

    def sort_players_for_next_round(self, players, round_number) -> List[Dict]:
        if round_number == 1:
            shuffle(players)
            return players
        else:
            players = sorted(
                players, key=lambda k: k["player_score"], reverse=True)
            return players

    def show_rounds(self, tournament_id: str) -> None:
        views = RoundViews()
        tournament = TournamentModel.load_by_id(id=tournament_id)
        t_rounds = RoundModel.get_tournament_rounds(tournament_id=tournament.get_id())
        t_rounds = [
            {
                "round": r,
                "games": GameModel.get_rounds_games(round_id=r.get_id())
            } for r in t_rounds
        ]
        views.show_rounds(rounds=t_rounds)
        input("Appuyez sur [Entrée] pour continuer")