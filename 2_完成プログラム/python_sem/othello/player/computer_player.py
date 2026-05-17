from .strategy import ComputerPlayerStrategy
from .player import Player

class ComputerPlayer(Player):
    """
    コンピュータプレイヤーを管理するクラス (Context)
    """

    def __init__(self, strategy: ComputerPlayerStrategy, stone_color):
        super().__init__(stone_color)
        self._strategy = strategy

    @property
    def strategy(self) -> ComputerPlayerStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ComputerPlayerStrategy) -> None:
        self._strategy = strategy

    def make_move(self, board):
        """
        設定された戦略に基づいて次の手を決定する
        """
        return self._strategy.choose_move(board, self.stone_color)
