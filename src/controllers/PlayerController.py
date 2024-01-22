from models.PlayerModel import PlayerModel
from views.player.PlayerViews import PlayerViews


class PlayerController:
    def __init__(self) -> None:
        self.views = PlayerViews()

    def index(self) -> None:
        """Show every player saved in the db"""
        players = PlayerModel.get_all()
        self.views.index(players=players)
