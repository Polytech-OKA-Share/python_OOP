from abc import ABC, abstractmethod

class Player(ABC):
    """
    プレイヤーの抽象基底クラス
    """
    def __init__(self, stone_color):
        self.stone_color = stone_color

    @abstractmethod
    def make_move(self, board):
        """
        次の手を決定する
        """
        pass
