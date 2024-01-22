from models.PlayerModel import PlayerModel


class GameModel:
    """Model class for the Game objects"""

    def __init__(self, player_1: PlayerModel, player_2: PlayerModel, player_1_score: float = 0.0, player_2_score: float = 0.0) -> None:
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1_score = player_1_score
        self.player_2_score = player_2_score
    
    def __repr__(self) -> str:
        return f"Joueur 1 : {self.player_1.fullname()} - {self.player_1_score} contre\
{self.player_2.fullname()} - {self.player_2_score}"

    def set_scores(self, winner: str) -> None:
        match winner:
            case "player_1":
                self.player_1_score = 1
                self.player_1.update_score(1)
            case "player_2":
                self.player_2_score = 1
                self.player_2.update_score(1)
            case "none":
                self.player_1_score = 0.5
                self.player_2_score = 0.5
                self.player_1.update_score(0.5)
                self.player_2.update_score(0.5)
    
    def get_winner(self) -> str | None:
        if self.player_1_score and self.player_2_score == 0:
            return None
        elif self.player_1_score and self.player_2_score == 0.5:
            return "Egalité"
        return (
            f"{self.player_1.fullname()}" if self.player_1_score > self.player_2_score else f"{self.player_2.fullname()}"
        )
    
    def get_players_names(self) -> str:
        return f"{self.player_1.fullname()} contre {self.player_2.fullname()}"
    