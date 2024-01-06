from models.PlayerModel import PlayerModel
from views.good_bye_screen import good_bye_screen
from views.add_player_menu_screen import add_player_menu_screen


class PlayerController:
    """Class to handle player related actions"""

    def __init__(self) -> None:
        self.player = None

    def register_player(self):
        """Function to create a new player"""
        # payload = player_form()
        payload = {
            "first_name": "Henry",
            "last_name": "Moore",
            "birth_date": "17031987",
            "national_chess_id": "UV23456",
        }
        new_player = PlayerModel(**payload)
        new_player.save()
        self.player = new_player
        return new_player

    def add_player_menu(self) -> PlayerModel | None:
        """Handles options to add a player to a tournament"""
        while True:
            try:
                user_choice = add_player_menu_screen()
                match user_choice:
                    case "1":
                        return self.register_player()
                    case "2":
                        pass
                    case _:
                        good_bye_screen(message="Aucun player n'a été ajouté.")
                        break
            except KeyError:
                print(
                    "Aucun choix ne correspond, \
    merci de sélectionner une des options du menu"
                )
                continue
