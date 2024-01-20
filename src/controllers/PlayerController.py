from models.PlayerModel import PlayerModel
from views.good_bye_screen import good_bye_screen
from views.add_player_menu_screen import add_player_menu_screen
from views.show_players_screen import show_players_screen
from views.player_form import player_form
from views.loading_screen import loading_screen
from views.alert_message import alert_message


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

    def add_player_menu(self) -> PlayerModel | None:
        """Handles options to add a player to a tournament"""
        while True:
            try:
                user_choice = add_player_menu_screen()
                match user_choice:
                    case "1":
                        return self.register_player()
                    case "2":
                        return self.load_player()
                    case "q":
                        good_bye_screen("Aucun joueur n'a été ajouté")
                        break
                    case _:
                        good_bye_screen(message="Aucun player n'a été ajouté.")
                        break
            except KeyError:
                alert_message(
                    message="Aucun choix ne correspond, \
    merci de sélectionner une des options du menu",
                    type="Error",
                )
                continue

    @classmethod
    def show_players(cls) -> None:
        """Function to list all the players already registered"""
        players_list = PlayerModel.get_all()
        if players_list:
            show_players_screen(players_list)
