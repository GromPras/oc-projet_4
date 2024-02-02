from models.GameModel import GameModel
from models.PlayerModel import PlayerModel
from models.RoundModel import RoundModel
from views.game.GameViews import GameViews
from views.shared.loading_screen import loading_screen
from utils.errors import SaveError


class GameController:
    def set_game_result(self, tournament_id: str) -> None:
        """Function to write the result of a game
        Takes the tournament's and round's ids to identify the round and update dependencies
        """
        current_round = RoundModel.get_tournament_rounds(
            tournament_id=tournament_id
        )[-1]
        games = GameModel.get_rounds_games(round_id=current_round.get_id())
        if games:
            # sort the games by id and retrieve games details
            sorted_games = sorted(games, key=lambda g: "game_id")
            games = [g.game_infos() for g in sorted_games]
            # load the views and the games for the user to choose from
            views = GameViews()
            games_menu = {
                str(index): game.__repr__()
                for index, game in enumerate(sorted_games, 1)
            }
            games_menu["q"] = "Annuler"
            user_choice = loading_screen(
                data=games_menu, title="Choisir le match :", raw_input=True
            )
            # get user's choice and test it
            # then prompt the user for the result of the game
            if user_choice:
                if user_choice == "q":
                    return
                game = sorted_games[int(user_choice) - 1]
                game_winner = views.game_winner(game=game.game_infos())
                # update data if the input is valid
                if isinstance(game_winner, str):
                    if game_winner == "none":
                        player_1 = PlayerModel.load_by_id(id=game.player_1_id)
                        player_2 = PlayerModel.load_by_id(id=game.player_2_id)
                        game = game.set_player_score(
                            player_1.national_chess_id, 0.5
                        )
                        game = game.set_player_score(
                            player_2.national_chess_id, 0.5
                        )
                        try:
                            game.update()
                        except SaveError as e:
                            print(e)
                        player_1.update_score(
                            tournament_id=tournament_id, value=0.5
                        )
                        player_2.update_score(
                            tournament_id=tournament_id, value=0.5
                        )
                        return
                    else:
                        winner = PlayerModel.load_by_id(id=game_winner)
                        game.set_player_score(game_winner, 1)
                        try:
                            game.update()
                        except SaveError as e:
                            print(e)
                        winner.update_score(
                            tournament_id=tournament_id, value=1
                        )
                        return
        return
