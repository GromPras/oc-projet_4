class PlayerModel:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: str,
        national_chess_id: str,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.national_chess_id = national_chess_id

    def __repr__(self) -> str:
        return f"#{self.national_chess_id} -\
{self.last_name} {self.first_name} - né(e) le : {self.birth_date}"
