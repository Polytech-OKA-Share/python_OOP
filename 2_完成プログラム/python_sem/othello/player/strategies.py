import random
from .strategy import ComputerPlayerStrategy

STRATEGIES = {}

def register_strategy(name):
    def decorator(cls):
        STRATEGIES[name] = cls
        return cls
    return decorator

@register_strategy("Easy (Random)")
class RandomStrategy(ComputerPlayerStrategy):
    """
    ランダムに手を選択する戦略
    """
    def choose_move(self, board, stone_color):
        valid_moves = board.get_valid_moves(stone_color)
        if not valid_moves:
            return None
        return random.choice(valid_moves)


@register_strategy("Normal (Greedy)")
class GreedyStrategy(ComputerPlayerStrategy):
    """
    最も多くの石を裏返せる手を選択する戦略
    """
    def choose_move(self, board, stone_color):
        valid_moves = board.get_valid_moves(stone_color)
        if not valid_moves:
            return None

        # 各有効な手について、裏返せる石の数を計算
        move_scores = {
            move: board.get_num_flippable_stones(move[0], move[1], stone_color)
            for move in valid_moves
        }

        # 最もスコアの高い手（複数ある場合はその中の一つ）を返す
        max_score = max(move_scores.values())
        best_moves = [move for move, score in move_scores.items() if score == max_score]

        return random.choice(best_moves)
