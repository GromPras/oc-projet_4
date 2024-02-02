import json
from typing import Any, Dict, Optional
from controllers.PlayerController import PlayerController
from controllers.RoundController import RoundController
from controllers.GameController import GameController
from models.GameModel import GameModel
from models.RoundModel import RoundModel
from models.PlayerModel import PlayerModel
from models.TournamentModel import TournamentModel
from views.shared.alert_message import alert_message
from views.shared.loading_screen import loading_screen
from views.tournament.TournamentViews import TournamentViews
from utils.errors import SaveError


class TournamentController():
    def __init__(self) -> None:
        self.views = TournamentViews()

    def new(self) -> None:
        """Calls the form to create a tournament
        then save a new Tournament
        and calls the show() function"""
        payload = self.views.new()
        new_tournament = TournamentModel(**payload)
        try:
            new_tournament.save()
            self.show(new_tournament.get_id())
        except SaveError as e:
            alert_message(message=str(e), type="Error")

    def load(self) -> None:
        """Calls the form to load a saved tournament
        then calls the show() function"""
        saved_tournaments = TournamentModel.get_all()
        load_menu = {
            str(index): tournament.__repr__()
            for index, tournament in enumerate(saved_tournaments, 1)
        }
        load_menu["q"] = "Annuler"
        user_choice = loading_screen(
            data=load_menu, title="Tounois sauvegardés :", raw_input=True
        )
        if user_choice and user_choice != "q":
            self.show(saved_tournaments[int(user_choice) - 1].get_id())
        else:
            return

    def show(self, tournament_id: str) -> None:
        tournament = TournamentModel.load_by_id(tournament_id)
        current_round_id = None
        if tournament.current_round > 0:
            t_rounds = RoundModel.get_tournament_rounds(tournament_id=tournament_id)
            sorted_rounds = sorted(t_rounds, key= lambda r: r.name)
            if tournament.current_round < tournament.number_of_rounds:
                current_round_id = sorted_rounds[tournament.current_round - 1].get_id()
        tournament_menu = self.load_tournament_menu(
            current_round=tournament.current_round,
            tournament_id=tournament.get_id(),
            current_round_id=current_round_id,
            max_rounds=tournament.number_of_rounds
        )
        menu_options = {key: option["name"]
                        for key, option in tournament_menu.items()}
        while True:
            self.views.show(tournament=tournament)
            user_choice = loading_screen(
                data=menu_options,
                title="Que voulez-vous faire ?",
                raw_input=True,
                clear_previous_screen=False
            )
            tournament_menu[user_choice]["controller"]()
            if tournament.current_round > tournament.number_of_rounds and user_choice == "3":
                break
            elif user_choice == "q" or user_choice == "Quitter":
                alert_message(
                    message="Merci d'avoir utilisé l'application. A bientôt!")
                break
            else:
                continue

    def start_round(self, tournament_id: str) -> None:
        """Increment the tournament current round
        and add a new round to the rounds list"""
        tournament = TournamentModel.load_by_id(tournament_id)
        t_players = PlayerModel.get_tournament_players(tournament_id=tournament.get_id())
        if not t_players:
            return
        elif len(t_players) < tournament.number_of_rounds * 2:
            alert_message(message="Pas assez de joueurs pour commencer", type="Error")
            return
        tournament.current_round += 1
        RoundController().new(
            tournament_id=tournament.get_id(),
            round_number=tournament.current_round
        )
        tournament.save()
        self.show(tournament_id=tournament.get_id())
        input("Appuyez sur [Entrée] pour continuer.")

    def end_tournament(self, tournament_id: str) -> None:
        tournament = TournamentModel.load_by_id(tournament_id)
        tournament.add_round()
        tournament.save()
        self.show(tournament_id=tournament.get_id())
        alert_message(message="Tournoi terminé")
        input("Appuyez sur [Entrée] pour continuer.")

    def archive_tournament(self, tournament_id: str) -> str:
        tournament = TournamentModel.load_by_id(id=tournament_id)
        t_players = PlayerModel.get_tournament_players(tournament_id=tournament.get_id())
        t_players_dict = [
            {
                "player": p["player"].__dict__,
                "player_score": p["player_score"]
            } for p in t_players
        ]
        t_rounds = RoundModel.get_tournament_rounds(tournament_id=tournament.get_id())
        t_rounds_dict = [r.__dict__ for r in t_rounds]
        for r in t_rounds_dict:
            games = GameModel.get_rounds_games(round_id=f"{r['round_id']}.json")
            if games:
                r["games"] = [g.to_dict() for g in games]
        t_dict = tournament.__dict__
        t_dict["players"] = sorted(t_players_dict, key= lambda p: p["player_score"], reverse=True)
        t_dict["rounds"] = t_rounds_dict
        try:
            with open(f"data/archives/{t_dict['starts']}_{t_dict['name']}.json", "w") as json_file:
                json.dump(t_dict, json_file)
            PlayerModel.remove_tournament_players(tournament_id=tournament.get_id())
            tournament.remove()
            for r in t_rounds:
                games = GameModel.get_rounds_games(round_id=r.get_id())
                if games:
                    GameModel.remove(r.get_id())
                r.remove()
        except SaveError as e:
            alert_message(message=str(e), type="Error")
        alert_message(message="Tournoi Archivé, vous pourez le consulter depuis le menu principal.", type="Info")
        return "Exit"

    def archives(self) -> None:
        tournaments = TournamentModel.get_archives()
        load_menu = {
            str(index): tournament
            for index, tournament in enumerate(tournaments, 1)
        }
        load_menu["q"] = "Annuler"
        user_choice = loading_screen(
            data=load_menu, title="Tounois archivés :", raw_input=True
        )
        if user_choice:
            tournament = TournamentModel.load_archive_by_name(tournaments[int(user_choice) - 1])
            self.views.archive(tournament)

    def load_tournament_menu(
        self, current_round: int, tournament_id: str, max_rounds: int, current_round_id: Optional[str] = None
    ) -> Dict[str, Dict[str, Any]]:
        """Returns a menu based on the current round number"""
        menu = {}
        if current_round == 0:
            menu = {
                "1": {
                    "name": "Afficher les joueurs du tournoi",
                    "controller": lambda: PlayerController().show_tournament_players(
                        tournament_id=tournament_id,
                        option="player_list"
                    ),
                },
                "2": {
                    "name": "Ajouter un joueur",
                    "controller": lambda: PlayerController().add_player_to_tournament(
                        tournament_id=tournament_id
                    ),
                },
                "3": {
                    "name": "Commencer le tournoi",
                    "controller": lambda: self.start_round(
                        tournament_id=tournament_id
                    ),
                },
            }

        if current_round >= 1:
            menu = {
                "1": {
                    "name": "Afficher les joueurs du tournoi",
                    "controller": lambda: PlayerController().show_tournament_players(
                        tournament_id=tournament_id,
                        option="player_list"
                    ),
                },
                "2": {
                    "name": "Afficher les tours",
                    "controller": lambda: RoundController().show_rounds(tournament_id=tournament_id),
                },
            }
            if current_round < max_rounds:
                menu.update(
                    {
                        "3": {
                            "name": "Inscrire les résultats d'un match",
                            "controller": lambda: GameController().set_game_result(round_id=current_round_id, tournament_id=tournament_id)
                        },
                        "4": {
                            "name": "Passer au tour suivant (tous les matchs du tour doivent être finis)",
                            "controller": lambda: RoundController().end_round(tournament_id=tournament_id, round_id=current_round_id)
                        }
                    }
                )
            elif current_round == max_rounds:
                menu.update(
                    {
                        "3": {
                            "name": "Inscrire les résultats d'un match",
                            "controller": lambda: GameController().set_game_result(round_id=current_round_id, tournament_id=tournament_id)
                        },
                        "4": {
                            "name": "Terminer le tournoi (tous les matchs du tour doivent être finis)",
                            "controller": lambda: self.end_tournament(tournament_id=tournament_id)
                        }
                    }
                )
            elif current_round > max_rounds:
                menu.update(
                    {
                        "3": {
                            "name": "Archiver le tournoi",
                            "controller": lambda: self.archive_tournament(tournament_id=tournament_id)
                        }
                    }
                )

        menu["q"] = {
            "name": "Quitter",
            "controller": lambda: None
        }
        return menu
