from typing import Dict
from views.alert_message import alert_message
from views.good_bye_screen import good_bye_screen


def loading_screen(data: Dict[str, str], title="", return_raw_input=False) -> str:
    """A function to print a list of item for the user to choose from"""
    while True:
        try:
            print(title)
            [print(f"{key}: {data[key]}") for key in data.keys()]

            user_choice = input("Sélectionnez un élément de la liste: ")
            if return_raw_input:
                return user_choice
            user_choice = data[user_choice]
            if user_choice == "Annuler":
                good_bye_screen(message="Retour au menu précédent")
                break
            return user_choice
        except KeyError:
            alert_message(
                message="Aucun choix ne correspond, \
merci de sélectionner une des options du menu",
                type="Error",
            )
            continue
