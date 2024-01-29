from random import shuffle
from typing import List, Dict, Optional
from models.GameModel import GameModel
from models.PlayerModel import PlayerModel
from models.RoundModel import RoundModel
from models.TournamentModel import TournamentModel
from utils.errors import SaveError
from views.round.RoundViews import RoundViews
from views.shared.alert_message import alert_message


class RoundController:
    def new(self, tournament_id: str, round_number: int) -> None:
        tournament = TournamentModel.load_by_id(id=tournament_id)
        t_rounds = RoundModel.get_tournament_rounds(tournament_id=tournament_id)
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
                players=sorted_players,
                t_rounds=t_rounds
            )
            [game.save() for game in round_games]
            new_round.save()
            alert_message(message="Nouveau tour", type="Info")
        except SaveError as e:
            alert_message(message=str(e), type="Info")

    def generate_pairs(
        self,
        round_id: str,
        round_number: int,
        number_of_pairs: int,
        players: List[Dict],
        t_rounds: Optional[List[RoundModel]] = None
    ) -> List[GameModel]:
        pairs = []
        if round_number == 1:
            for i in range(0, len(players), 2):
                pairs.append(GameModel(
                    round_id=round_id,
                    player_1_id=players[i]["player_id"],
                    player_1_score=players[i]["player_score"],
                    player_2_id=players[i + 1]["player_id"],
                    player_2_score=players[i + 1]["player_score"]
                ))
            return pairs
        else:
            for _ in range(number_of_pairs):
                currently_paired = []
                for g in pairs:
                    currently_paired.append(g.player_1_id)
                    currently_paired.append(g.player_2_id)
                remaining_players = filter(
                    lambda p: p["player_id"] not in currently_paired,
                    players
                )
                previous_pairs = self.get_previous_pairs(t_rounds=t_rounds)
                for player in remaining_players:
                    opponents = filter(
                        lambda p: player["player_id"] != p["player_id"],
                        remaining_players
                    )

                    player_2 = self.find_new_opponent(
                        player_1_id=player["player_id"],
                        previous_pairs=previous_pairs,
                        possible_opponents=list(opponents)
                    )

                    pairs.append(GameModel(
                        round_id=round_id,
                        player_1_id=player["player_id"],
                        player_1_score=0,
                        player_2_id=player_2,
                        player_2_score=0
                    ))
            return pairs

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
    
    def end_round(self, tournament_id: str, round_id: str) -> None:
        current_round = RoundModel.load_by_id(round_id=round_id)
        tournament = TournamentModel.load_by_id(id=tournament_id)
        tournament.add_round()
        tournament.save()
        current_round.set_round_end()
        current_round.save()
        self.new(tournament_id=tournament.get_id(), round_number=tournament.current_round)

    def get_previous_pairs(self, t_rounds: List[RoundModel]) -> List[List[str]]:
        pairs = []
        for r in t_rounds:
            print(r)
            previous_games = GameModel.get_rounds_games(round_id=r.get_id())
            for g in previous_games:
                pairs.append([g.player_1_id, g.player_2_id])
        
        return pairs
    
    def find_new_opponent(self, player_1_id: str, previous_pairs: List[List[str]], possible_opponents: List[str]) -> str:
        new_opponent = None
        for o in possible_opponents:
            if (player_1_id, o["player_id"]) not in previous_pairs:
                new_opponent = o["player_id"]
                return new_opponent
        return None