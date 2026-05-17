from abc import ABC, abstractmethod

class ComputerPlayerStrategy(ABC):
    """
    コンピュータプレイヤーの思考ロ-ジックの抽象基底クラス (Strategy)
    """

    @abstractmethod
    def choose_move(self, board, stone_color):
        """
        利用可能な手の中から次の手を選択する

        :param board: 現在のゲーム盤 (Board)
        :param stone_color: コンピュータの石の色 (Stone)
        :return: (x, y) タプルで表される選択した手
        """
        pass
