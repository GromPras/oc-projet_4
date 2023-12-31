def add_player_menu_screen() -> str:
    """Displays the options to add a player to a tournament"""
    options = {
        "1": "Enregistrer un nouveau joueur",
        "2": "Charger un joueur depuis la liste",
    }
    print("Ajouter un joueur au tournoi : ")
    [print(f"{key} : {options[key]}") for key in options.keys()]
    return input("Que voulez-vous faire ?: ")
