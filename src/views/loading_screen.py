from typing import Dict


def loading_screen(data: Dict[str, str]) -> str:
    """A function to print a list of item for the user to choose from"""
    [print(f"{key}: {data[key]}") for key in data.keys()]
    return input("Sélectionnez un élément de la liste: ")
