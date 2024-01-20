from models.RoundModel import RoundModel
from models.PlayerModel import PlayerModel
from models.TournamentModel import TournamentModel
from views.alert_message import alert_message
from views.loading_screen import loading_screen


class RoundController:
    def write_match_result(self, tournament: TournamentModel) -> TournamentModel:
        """Function to write the result of a match"""
        current_round = tournament.rounds_list[tournament.current_round - 1]
        if not isinstance(current_round, RoundModel):
            current_round = RoundModel(**current_round)
        games = {
            str(index): game.get_players()
            for index, game in enumerate(current_round.games, 1)
        }
        games["q"] = "Annuler"
        user_choice = loading_screen(
            games, title="Sélectionnez un match : ",
            return_raw_input=True
        )
        if user_choice:
            game_index = int(user_choice) - 1
            if not current_round.games[game_index]:
                raise KeyError
            game = current_round.games[game_index]
            print(game)
            results = {
                "1": game.player_1.fullname(),
                "2": game.player_2.fullname(),
                "3": "Egalité",
            }
            result = loading_screen(
                results, title="Qui à gagné le match ?", return_raw_input=True
            )
            if not isinstance(tournament.players[0], PlayerModel):
                tournament.players = [
                    PlayerModel(**player)
                    for player in tournament.players
                ]
            match result:
                case "1":
                    alert_message(message="Le joueur 1 gagne", type="Info")
                    game.set_score(winner="player_1")
                    [
                        player.update_score(1)
                        for player in tournament.players
                        if player.national_chess_id
                        == game.player_1.national_chess_id
                    ]
                    tournament.save()
                    return tournament
                case "2":
                    alert_message(message="Le joueur 2 gagne", type="Info")
                    game.set_score(winner="player_2")
                    [
                        player.update_score(1)
                        for player in tournament.players
                        if player.national_chess_id
                        == game.player_2.national_chess_id
                    ]
                    tournament.save()
                    return tournament
                case "3":
                    alert_message(message="Egalité", type="Info")
                    game.set_score(winner="none")
                    players_id = []
                    players_id.append(game.player_1.national_chess_id)
                    players_id.append(game.player_2.national_chess_id)
                    for player in tournament.players:
                        if player.national_chess_id in players_id:
                            player.update_score(0.5)
                    tournament.save()
                    return tournament
                case _:
                    return
