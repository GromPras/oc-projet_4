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
    print("""
  ____ _                      ____           _            
 / ___| |__   ___  ___ ___   / ___|___ _ __ | |_ ___ _ __ 
| |   | '_ \ / _ \/ __/ __| | |   / _ \ '_ \| __/ _ \ '__|
| |___| | | |  __/\__ \__ \ | |__|  __/ | | | ||  __/ |   
 \____|_| |_|\___||___/___/  \____\___|_| |_|\__\___|_|   """)
    print()
    [print(f"{option}: {options[option]}") for option in options.keys()]

    return input("Que voulez-vous faire? ")
