from connect_four.agents.victor import Board
from connect_four.agents.victor import Square


class Baseinverse:
    def __init__(self, playable1: Square, playable2: Square):
        if playable1 == playable2:
            raise ValueError(playable1, "==", playable2)

        self.squares = frozenset([
            playable1,
            playable2,
        ])

    def __eq__(self, other):
        if isinstance(other, Baseinverse):
            return self.squares == other.squares
        return False

    def __hash__(self):
        return self.squares.__hash__()


def baseinverse(board: Board):
    baseinverses = set()
    playable_squares = board.playable_squares()

    for playable1 in playable_squares:
        for playable2 in playable_squares:
            if playable1 != playable2:
                baseinverses.add(Baseinverse(playable1, playable2))
    return baseinverses
