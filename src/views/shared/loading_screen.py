from typing import Dict
from utils.functions import clear_screen
from views.shared.alert_message import alert_message


def loading_screen(
    data: Dict[str, str],
    title: str,
    raw_input=True,
    clear_previous_screen=True
) -> str:
    """A function to print a list of item for the user to choose from
    Can return the raw input, a string or None
    """
    if clear_previous_screen:
        clear_screen()
    while True:
        try:
            print(title)
            [print(f"{key}: {data[key]}") for key in data.keys()]

            user_choice = input("Sélectionnez un élément de la liste: ")
            if raw_input:
                return user_choice
            user_choice = data[user_choice]
            if user_choice == "Annuler" or "q":
                alert_message(message="Retour au menu précédent", type="Info")
                break
            return user_choice
        except KeyError:
            alert_message(
                message="Aucun choix ne correspond, \
merci de sélectionner une des options du menu",
                type="Error",
            )
            continue
