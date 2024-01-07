import re
from datetime import datetime
from typing import Any


class FormValidationError(ValueError):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message


def validate_field(validation_func) -> Any:
    while True:
        value = None
        try:
            value = validation_func
            break
        except ValueError as err:
            print(err)
            continue
    return value


@validate_field
def field_length(value: str, length: int) -> str:
    """Function to test the length of a field"""
    if value == "" or len(value) < length:
        raise FormValidationError(
            message=f"Ce champ doit contenir au moins {length} caractères"
        )
    return value


@validate_field
def field_date(value: str) -> str:
    sanitized_date = (
        value.replace("_", "")
        .replace("/", "")
        .replace(" ", "")
        .replace("-", "")
    )
    field_length(sanitized_date, length=8)
    if not datetime.strptime(sanitized_date, "%d%m%Y").date():
        raise FormValidationError(
            message="La date doit être au format: jjmmaaaa"
        )

    return sanitized_date


@validate_field
def field_number(value: str) -> int:
    field_length(value, length=1)
    if not int(value):
        raise FormValidationError(
            message="Le nombre de rondes doit être un nombre"
        )
    return int(value) if int(value) > 4 else 4


@validate_field
def national_chess_id(value: str) -> str:
    field_length(value, length=7)
    if not re.fullmatch(r"[A-Za-z]{2}\d{5}", value):
        raise FormValidationError(
            message="Format de l'identifiant national d'échecs invalide \
                Format valide: AA00000"
        )
    return value
