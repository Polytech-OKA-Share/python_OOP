import unittest
from othello.board import Board
from othello.stone import Stone


class TestBoard(unittest.TestCase):
    """
    Boardクラスのテスト
    """

    def setUp(self):
        """
        テストの前にBoardインスタンスを作成する
        """
        self.board = Board()

    def test_initial_board(self):
        """
        盤面の初期状態をテストする
        """
        self.assertEqual(self.board.grid[3][3], Stone.WHITE)
        self.assertEqual(self.board.grid[4][4], Stone.WHITE)
        self.assertEqual(self.board.grid[3][4], Stone.BLACK)
        self.assertEqual(self.board.grid[4][3], Stone.BLACK)
        black_stones, white_stones = self.board.count_stones()
        self.assertEqual(black_stones, 2)
        self.assertEqual(white_stones, 2)

    def test_get_valid_moves_initial(self):
        """
        ゲーム開始時の黒の有効な手をテストする
        """
        valid_moves = self.board.get_valid_moves(Stone.BLACK)
        self.assertCountEqual(valid_moves, [(2, 3), (3, 2), (4, 5), (5, 4)])

    def test_place_stone_and_flip(self):
        """
        石を置いて裏返す処理をテストする
        """
        # 黒が (3, 2) に石を置く
        self.board.place_stone(3, 2, Stone.BLACK)
        # (3, 3) の白石が黒に裏返るはず
        self.assertEqual(self.board.grid[3][3], Stone.BLACK)
        # 石の数を確認
        black_stones, white_stones = self.board.count_stones()
        self.assertEqual(black_stones, 4)
        self.assertEqual(white_stones, 1)

    def test_is_valid_move(self):
        """
        is_valid_moveメソッドをテストする
        """
        self.assertTrue(self.board.is_valid_move(3, 2, Stone.BLACK))
        self.assertFalse(self.board.is_valid_move(0, 0, Stone.BLACK))
        self.assertFalse(self.board.is_valid_move(3, 3, Stone.BLACK)) # Already occupied

    def test_no_valid_moves(self):
        """
        有効な手がない状況をテストする
        """
        # 手動で盤面を埋める
        self.board.grid = [[Stone.BLACK for _ in range(8)] for _ in range(8)]
        self.assertFalse(self.board.get_valid_moves(Stone.WHITE))


if __name__ == '__main__':
    unittest.main()
