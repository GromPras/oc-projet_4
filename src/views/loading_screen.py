from typing import List


def loading_screen(data: List) -> str:
    """A function to print a list of item for the user to choose from"""
    [print(f"{index}: {item}") for index, item in enumerate(data)]
    return input("Sélectionnez un élément de la liste: ")
