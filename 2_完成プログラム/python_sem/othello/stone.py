from enum import Enum, auto


class Stone(Enum):
    """
    石の状態を定義するクラス
    """
    EMPTY = auto()
    BLACK = auto()
    WHITE = auto()
