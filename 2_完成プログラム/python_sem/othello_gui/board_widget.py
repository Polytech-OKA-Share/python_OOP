from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, pyqtSignal, QRect

from othello.stone import Stone


class BoardWidget(QWidget):
    """
    オセロ盤を描画するウィジェット
    """
    move_made = pyqtSignal(int, int)

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.setMinimumSize(600, 600)
        self.signals_connected = False

    def mousePressEvent(self, event):
        """
        クリックされたときに呼ばれる
        """
        if not self.game or self.window().game_over:
            return

        # 現在のプレイヤーが人間でなければ何もしない
        from othello.player.human_player import HumanPlayer
        if not isinstance(self.window().current_player, HumanPlayer):
            return

        grid_size = self.game.board.size
        cell_width = self.width() / grid_size
        cell_height = self.height() / grid_size

        x = int(event.position().x() // cell_width)
        y = int(event.position().y() // cell_height)

        if (x, y) in self.game.board.get_valid_moves(self.window().current_player.stone_color):
            self.move_made.emit(x, y)

    def paintEvent(self, event):
        """
        盤面を描画する
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QColor("#008000"))

        grid_size = self.game.board.size
        cell_width = self.width() / grid_size
        cell_height = self.height() / grid_size
        painter.setPen(QPen(QColor(Qt.GlobalColor.black), 2))
        for i in range(grid_size + 1):
            painter.drawLine(int(i * cell_width), 0, int(i * cell_width), self.height())
            painter.drawLine(0, int(i * cell_height), self.width(), int(i * cell_height))

        for y in range(grid_size):
            for x in range(grid_size):
                stone = self.game.board.grid[y][x]
                if stone != Stone.EMPTY:
                    rect = self.cell_rect(x, y)
                    if stone == Stone.BLACK:
                        painter.setBrush(QBrush(Qt.GlobalColor.black))
                    else:
                        painter.setBrush(QBrush(Qt.GlobalColor.white))
                    painter.drawEllipse(rect)

    def cell_rect(self, x, y):
        """
        指定されたセルの描画範囲 (QRect) を計算する
        """
        grid_size = self.game.board.size
        cell_width = self.width() / grid_size
        cell_height = self.height() / grid_size
        padding = 5

        return QRect(
            int(x * cell_width + padding),
            int(y * cell_height + padding),
            int(cell_width - 2 * padding),
            int(cell_height - 2 * padding)
        )
