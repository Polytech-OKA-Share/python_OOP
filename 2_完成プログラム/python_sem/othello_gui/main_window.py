from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtCore import Qt, QTimer

from othello.game import Game
from othello.stone import Stone
from othello.player.player import Player
from othello.player.human_player import HumanPlayer
from othello.player.computer_player import ComputerPlayer
from othello.player.strategies import STRATEGIES
from .board_widget import BoardWidget
from .new_game_dialog import NewGameDialog


class MainWindow(QMainWindow):
    """
    ゲームのメインウィンドウ
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Othello")
        self.setGeometry(100, 100, 600, 700) # メニューバーの分だけ少し高さを増やす

        self._create_menu_bar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.status_label.font()
        font.setPointSize(14)
        self.status_label.setFont(font)
        layout.addWidget(self.status_label)

        # Game object will be created in start_new_game
        self.board_widget = BoardWidget(None)
        layout.addWidget(self.board_widget)

        self.start_new_game()
        self.show()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        game_menu = menu_bar.addMenu("&Game")

        new_game_action = QAction("&New Game", self)
        new_game_action.triggered.connect(self.start_new_game)
        game_menu.addAction(new_game_action)

        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.close)
        game_menu.addAction(exit_action)

    def start_new_game(self):
        dialog = NewGameDialog(self)
        if dialog.exec():
            game_mode, ai_difficulty = dialog.get_settings()

            self.game = Game()
            self.board_widget.game = self.game
            if not self.board_widget.signals_connected:
                self.board_widget.move_made.connect(self.play_turn_and_update)
                self.board_widget.signals_connected = True

            self.player1 = HumanPlayer(Stone.BLACK)
            if game_mode == 'pvc':
                strategy_class = STRATEGIES.get(ai_difficulty)
                strategy = strategy_class()
                self.player2 = ComputerPlayer(strategy, Stone.WHITE)
            else:
                self.player2 = HumanPlayer(Stone.WHITE)

            self.current_player = self.player1
            self.game_over = False
            self.update_status()
            self.board_widget.update()
            self.handle_next_turn() # コンピュータが先手の場合の対応
        else:
            # ダイアログがキャンセルされた場合、アプリケーションを終了するか、何もしないか
            # 初回起動時にキャンセルされた場合は終了する
            if not hasattr(self, 'game'):
                 self.close()

    def play_turn_and_update(self, x, y):
        if self.game_over:
            return

        self.game.play_turn(x, y)
        self.board_widget.update()
        self.handle_next_turn()

    def handle_next_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        self.game.current_player = self.current_player.stone_color
        self.update_status()

        if self.game.is_game_over():
            self.game_over = True
            self.show_game_over_dialog()
            return

        if not self.game.board.get_valid_moves(self.current_player.stone_color):
            player_name = "Black" if self.current_player.stone_color == Stone.BLACK else "White"
            QMessageBox.information(self, "Pass", f"{player_name} has no valid moves. Turn is passed.")
            self.handle_next_turn() # 相手のターンへ
            return

        if isinstance(self.current_player, ComputerPlayer):
            QTimer.singleShot(500, self.trigger_computer_move)

    def trigger_computer_move(self):
        if self.game_over:
            return

        move = self.current_player.make_move(self.game.board)
        if move:
            self.play_turn_and_update(move[0], move[1])

    def show_game_over_dialog(self):
        winner = self.game.get_winner()
        if winner:
            winner_name = "Black" if winner == Stone.BLACK else "White"
            msg = f"Winner: {winner_name}!"
        else:
            msg = "It's a draw!"

        black_stones, white_stones = self.game.board.count_stones()
        full_msg = f"{msg}\n\nFinal score: Black {black_stones} - White {white_stones}"
        QMessageBox.information(self, "Game Over", full_msg)

    def update_status(self):
        black_stones, white_stones = self.game.board.count_stones()
        if self.game_over:
            status_text = f"Game Over!   |   Final Score: Black {black_stones} - White {white_stones}"
        else:
            player_name = "Black" if self.game.current_player == Stone.BLACK else "White"
            status_text = f"Current Player: {player_name}   |   Score: Black {black_stones} - White {white_stones}"
        self.status_label.setText(status_text)
