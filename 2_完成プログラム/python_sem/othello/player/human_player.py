from .player import Player

class HumanPlayer(Player):
    """
    人間のプレイヤーを表すクラス
    """
    def make_move(self, board):
        """
        人間の手はGUIイベントによって処理されるため、このメソッドでは何もしない
        """
        pass
