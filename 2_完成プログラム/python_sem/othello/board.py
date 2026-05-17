from othello.stone import Stone


class Board:
    """
    オセロの盤面を管理するクラス
    """

    def __init__(self, size=8):
        """
        盤面を初期化する
        """
        self.size = size
        self.grid = [[Stone.EMPTY for _ in range(size)] for _ in range(size)]
        # 初期配置
        center = size // 2
        self.grid[center - 1][center - 1] = Stone.WHITE
        self.grid[center][center] = Stone.WHITE
        self.grid[center - 1][center] = Stone.BLACK
        self.grid[center][center - 1] = Stone.BLACK

    def __str__(self):
        """
        盤面を文字列で表現する
        """
        board_str = "  " + " ".join(map(str, range(self.size))) + "\n"
        for i, row in enumerate(self.grid):
            board_str += str(i) + " "
            for stone in row:
                if stone == Stone.EMPTY:
                    board_str += ". "
                elif stone == Stone.BLACK:
                    board_str += "B "
                elif stone == Stone.WHITE:
                    board_str += "W "
            board_str += "\n"
        return board_str

    def _check_direction(self, x, y, dx, dy, stone_color):
        """
        指定された方向で裏返せる石のリストを取得する
        """
        opponent_color = Stone.WHITE if stone_color == Stone.BLACK else Stone.BLACK
        stones_to_flip = []
        nx, ny = x + dx, y + dy

        while 0 <= nx < self.size and 0 <= ny < self.size:
            if self.grid[ny][nx] == opponent_color:
                stones_to_flip.append((nx, ny))
            elif self.grid[ny][nx] == stone_color:
                return stones_to_flip
            else:  # Stone.EMPTY or out of bounds
                return []
            nx, ny = nx + dx, ny + dy
        return []

    def _get_flippable_stones(self, x, y, stone_color):
        """
        指定した場所に石を置いた場合に裏返せる石のリストを取得する
        """
        if self.grid[y][x] != Stone.EMPTY:
            return []

        flippable_stones = []
        # 8方向をチェック
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            flippable_stones.extend(self._check_direction(x, y, dx, dy, stone_color))

        return flippable_stones

    def get_num_flippable_stones(self, x, y, stone_color):
        """
        指定した場所に石を置いた場合に裏返せる石の数を返す
        """
        return len(self._get_flippable_stones(x, y, stone_color))

    def is_valid_move(self, x, y, stone_color):
        """
        指定された場所に石を置けるかどうかを判定する
        """
        return bool(self._get_flippable_stones(x, y, stone_color))

    def place_stone(self, x, y, stone_color):
        """
        指定された場所に石を置き、相手の石を裏返す
        """
        flippable_stones = self._get_flippable_stones(x, y, stone_color)
        if not flippable_stones:
            return False

        self.grid[y][x] = stone_color
        for flip_x, flip_y in flippable_stones:
            self.grid[flip_y][flip_x] = stone_color
        return True

    def get_valid_moves(self, stone_color):
        """
        指定された色の石が置ける全ての場所を取得する
        """
        valid_moves = []
        for y in range(self.size):
            for x in range(self.size):
                if self.is_valid_move(x, y, stone_color):
                    valid_moves.append((x, y))
        return valid_moves

    def count_stones(self):
        """
        盤上の石の数を数える
        """
        black_stones = 0
        white_stones = 0
        for row in self.grid:
            for stone in row:
                if stone == Stone.BLACK:
                    black_stones += 1
                elif stone == Stone.WHITE:
                    white_stones += 1
        return black_stones, white_stones
