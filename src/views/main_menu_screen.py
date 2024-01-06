def main_menu_screen() -> str:
    """A function to welcome the user"""
    options = {
        "1": "Créer un tournoi",
        "2": "Charger un tournoi",
        "q": "Quitter",
    }
    [print(f"{option}: {options[option]}") for option in options.keys()]

    return input("Que voulez-vous faire? ")
