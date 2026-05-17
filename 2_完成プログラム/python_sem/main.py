import time
from othello.game import Game
from othello.stone import Stone
from othello.player.human_player import HumanPlayer
from othello.player.computer_player import ComputerPlayer
from othello.player.strategies import STRATEGIES


def _select_game_settings():
    """
    ユーザーにゲームモードとAIの難易度を選択させる
    """
    # モード選択
    while True:
        mode = input("Select game mode (1: Human vs Human, 2: Human vs Computer): ")
        if mode in ["1", "2"]:
            break
        print("Invalid input. Please enter 1 or 2.")

    player1 = HumanPlayer(Stone.BLACK)
    player2 = None

    if mode == "1":
        player2 = HumanPlayer(Stone.WHITE)
        print("\nStarting Human vs Human game.")
    else:
        # AI難易度選択
        strategy_names = list(STRATEGIES.keys())
        while True:
            print("\nSelect computer difficulty:")
            for i, name in enumerate(strategy_names):
                print(f"{i + 1}: {name}")

            try:
                choice = int(input(f"Enter number (1-{len(strategy_names)}): "))
                if 1 <= choice <= len(strategy_names):
                    strategy_name = strategy_names[choice - 1]
                    strategy_class = STRATEGIES[strategy_name]
                    player2 = ComputerPlayer(strategy_class(), Stone.WHITE)
                    print(f"\nStarting Human vs Computer ({strategy_name}) game.")
                    break
                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a valid number.")

    return player1, player2


def game_loop(game, player1, player2):
    """
    CUIでのゲームのメインループ
    """
    current_player = player1

    while not game.is_game_over():
        print(game.board)
        player_name = "Black" if current_player.stone_color == Stone.BLACK else "White"
        print(f"Current player: {player_name}")

        valid_moves = game.board.get_valid_moves(current_player.stone_color)
        if not valid_moves:
            print("No valid moves. Passing the turn.")
            game.switch_player() # Gameオブジェクトにプレイヤー切り替えを任せる
            current_player = player2 if current_player == player1 else player1
            continue

        if isinstance(current_player, HumanPlayer):
            print("Valid moves:", valid_moves)
            while True:
                try:
                    move_str = input("Enter your move (x,y): ")
                    x_str, y_str = move_str.split(',')
                    x, y = int(x_str), int(y_str)
                    if (x, y) in valid_moves:
                        game.play_turn(x, y)
                        break
                    else:
                        print("Invalid move. Please choose from the valid moves.")
                except ValueError:
                    print("Invalid input format. Please use 'x,y'.")
        else: # ComputerPlayer
            print("Computer is thinking...")
            time.sleep(1)
            move = current_player.make_move(game.board)
            print(f"Computer plays: {move}")
            game.play_turn(move[0], move[1])

        current_player = player2 if current_player == player1 else player1


def show_result(game):
    """
    ゲームの結果を表示する
    """
    print("\n--- Game Over ---")
    print(game.board)
    winner = game.get_winner()
    if winner:
        winner_name = "Black" if winner == Stone.BLACK else "White"
        print(f"Winner: {winner_name}!")
    else:
        print("It's a draw!")

    black_stones, white_stones = game.board.count_stones()
    print(f"Final score: Black {black_stones} - White {white_stones}")


def main():
    """
    CUIでオセロゲームを実行する
    """
    player1, player2 = _select_game_settings()
    game = Game()
    game_loop(game, player1, player2)
    show_result(game)


if __name__ == "__main__":
    main()
