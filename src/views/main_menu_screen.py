from utils.functions import clear_screen


def main_menu_screen() -> str:
    """A function to welcome the user"""
    clear_screen()
    options = {
        "1": "Créer un tournoi",
        "2": "Charger un tournoi",
        "3": "Afficher tous les joueurs",
        "q": "Quitter",
    }
    print("Bienvenue dans ChessCenter :")
    [print(f"{option}: {options[option]}") for option in options.keys()]

    return input("Que voulez-vous faire? ")
