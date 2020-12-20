from connect_four.agents.victor import Board
from connect_four.agents.victor import Square
from connect_four.envs.connect_four_env import ConnectFourEnv


class Claimeven:
    def __init__(self, upper: Square, lower: Square):
        self.upper = upper
        self.lower = lower

    def __eq__(self, other):
        if isinstance(other, Claimeven):
            return self.upper == other.upper and self.lower == other.lower
        return False

    def __hash__(self):
        return self.upper.__hash__() * 31 + self.lower.__hash__()


def claimeven(board: Board):
    claimevens = set()

    for row in range(0, ConnectFourEnv.M, 2):
        for col in range(ConnectFourEnv.N):
            upper = Square(row, col)
            lower = Square(row + 1, col)

            if board.is_empty(upper) and board.is_empty(lower):
                claimevens.add(Claimeven(upper, lower))

    return claimevens
