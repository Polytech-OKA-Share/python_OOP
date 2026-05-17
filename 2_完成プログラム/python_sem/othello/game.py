from othello.board import Board
from othello.stone import Stone


class Game:
    """
    オセロゲームの進行を管理するクラス
    """

    def __init__(self):
        """
        ゲームを初期化する
        """
        self.board = Board()
        self.current_player = Stone.BLACK

    def switch_player(self):
        """
        プレイヤーを切り替える
        """
        self.current_player = Stone.WHITE if self.current_player == Stone.BLACK else Stone.BLACK

    def play_turn(self, x, y):
        """
        指定された場所に石を置いてターンを進める
        """
        if self.board.place_stone(x, y, self.current_player):
            self.switch_player()
            return True
        return False

    def is_game_over(self):
        """
        ゲームが終了したかどうかを判定する
        """
        # どちらのプレイヤーも置ける場所がない場合に終了
        black_moves = self.board.get_valid_moves(Stone.BLACK)
        white_moves = self.board.get_valid_moves(Stone.WHITE)
        return not black_moves and not white_moves

    def get_winner(self):
        """
        勝者を判定する
        """
        black_stones, white_stones = self.board.count_stones()
        if black_stones > white_stones:
            return Stone.BLACK
        elif white_stones > black_stones:
            return Stone.WHITE
        else:
            return None  # 引き分け
