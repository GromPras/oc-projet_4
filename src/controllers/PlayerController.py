from models.PlayerModel import PlayerModel
from views.good_bye_screen import good_bye_screen
from views.show_players_screen import show_players_screen
from views.player_form import player_form
from views.loading_screen import loading_screen


class PlayerController:
    """Class to handle player related actions"""

    def __init__(self) -> None:
        self.player = None

    def register_player(self):
        """Function to create a new player"""
        payload = player_form()
        new_player = PlayerModel(**payload)
        self.player = new_player
        new_player.save()
        return new_player

    def load_player(self) -> PlayerModel | None:
        """Functions to load a player saved in a json file"""
        saved_players = PlayerModel.get_all()
        if saved_players:
            player_list = {
                str(index): repr(player)
                for index, player in enumerate(saved_players, 1)
            }
            player_list["q"] = "Annuler"
            user_choice = loading_screen(
                player_list, title="Joueurs enregistrés :")
            if user_choice:
                self.player = PlayerModel.load_by_id(user_choice)
                return self.player
            else:
                return

    def add_player_menu(self) -> PlayerModel | None:
        """Handles options to add a player to a tournament"""
        options = {
            "1": {
                "name": "Enregistrer un nouveau joueur",
                "func": lambda: self.register_player(),
            },
            "2": {
                "name": "Charger un joueur depuis la liste",
                "func": lambda: self.load_player(),
            },
            "3": {
                "name": "Annuler",
                "func": lambda: good_bye_screen(message="Aucun joueur n'a été ajouté")
            }
        }
        user_choice = loading_screen(
            data={key: option["name"] for key, option in options.items()},
            return_raw_input=True
        )
        if user_choice:
            return options[user_choice]["func"]()

    @classmethod
    def show_players(cls) -> None:
        """Function to list all the players already registered"""
        players_list = PlayerModel.get_all()
        if players_list:
            show_players_screen(players_list)
