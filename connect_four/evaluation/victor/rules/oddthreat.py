from typing import List, Set

from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.rules import Rule
from connect_four.game import Square
from connect_four.problem import Group

import warnings


class Oddthreat(Rule):
    def __init__(self, group: Group, empty_square: Square, directly_playable_square: Square):
        self.group = group
        self.empty_square = empty_square
        self.directly_playable_square = directly_playable_square

    def __eq__(self, other):
        if isinstance(other, Oddthreat):
            return self.group == other.group and self.empty_square == other.empty_square
        return False

    def __hash__(self):
        return self.group.__hash__() * 97 + self.empty_square.__hash__() * 31

    def solves(self, group: Group) -> bool:
        for square in group.squares:
            if square.col == self.empty_square.col:
                # If group contains an odd square at or below the empty square of this Oddthreat but above the directly
                # playable square of this Oddthreat, it can be refuted.
                if self.empty_square.row <= square.row < self.directly_playable_square.row and square.row % 2 == 1:
                    return True

                # If group contains a square above the empty square of this Oddthreat, it can be refuted.
                if self.empty_square.row > square.row:
                    return True

        return False

    def is_useful(self, groups: Set[Group]) -> bool:
        return True

    def find_problems_solved(self, groups_by_square_by_player: List[List[List[Set[Group]]]]) -> Set[Group]:
        """Finds all Problems this Rule solves.

        Args:
            groups_by_square_by_player (List[List[List[Set[Group]]]]): a 3D array of a Set of Groups.
                1. The first dimension is the player.
                2. The second dimension is the row.
                3. The third dimension is the col.

                For a given player and a given (row, col),
                you can retrieve all Groups that player can win from that Square with:
                    set_of_possible_winning_groups_at_player_row_col = groups_by_square_by_player[player][row][col]

        Returns:
            problems_solved (Set[Group]): All Problems in square_to_groups this Rule solves.
        """
        warnings.warn("find_problems_solved is deprecated. use solves() instead", DeprecationWarning)
        problems_solved = set()

        # Add Groups containing any odd Square up to the Odd Threat that are not directly playable.
        for row in range(self.empty_square.row, self.directly_playable_square.row, 2):
            problems_solved.update(groups_by_square_by_player[1][row][self.empty_square.col])

        # Add Groups containing any Squares above the odd Threat.
        for row in range(0, self.empty_square.row, 1):
            problems_solved.update(groups_by_square_by_player[1][row][self.empty_square.col])

        # noinspection PyTypeChecker
        return problems_solved


def find_all_oddthreats(board: Board) -> Set[Oddthreat]:
    """find_all_oddthreats returns all OddThreats for White.

    Args:
        board (Board): a Board instance.

    Returns:
        odd_group (Set[Oddthreat]): a set of Oddthreats for board.
    """
    directly_playable_squares = board.playable_squares()
    # Iterate through all groups that belong to White.
    odd_threats = set()
    for group in board.potential_groups(player=0):
        empty_squares = empty_squares_of_group(board, group)
        # If there is only 1 empty square in the group, the square is not directly playable, and it is an odd square:
        if (len(empty_squares) == 1 and
                empty_squares[0] not in directly_playable_squares and
                empty_squares[0].row % 2 == 1):
            empty_square = empty_squares[0]
            odd_threat = Oddthreat(
                group=group,
                empty_square=empty_square,
                directly_playable_square=board.playable_square(col=empty_square.col)
            )
            odd_threats.add(odd_threat)
    return odd_threats


def empty_squares_of_group(board: Board, group: Group) -> List[Square]:
    """Returns a list of all empty Squares that belong to group.

    Args:
        board (Board): a Board instance.
        group (Group): a Group on Board.

    Returns:
        empty_squares (List<Square>): a list of empty Squares that belong to group.
    """
    empty_squares = []
    for square in group.squares:
        if board.is_empty(square):
            empty_squares.append(square)
    return empty_squares


class OddthreatManager:
    def __init__(self, board: Board):
        self.oddthreats = find_all_oddthreats(board=board)

    def move(self, player: int, square: Square, board: Board):
        board.state[player][square.row][square.col] = 1

        new_oddthreats = find_all_oddthreats(board=board)

        removed_oddthreats = self.oddthreats - new_oddthreats
        added_oddthreats = new_oddthreats - self.oddthreats

        self.oddthreats = new_oddthreats

        board.state[player][square.row][square.col] = 0

        return removed_oddthreats, added_oddthreats

    def undo_move(self, player: int, square: Square, board: Board):
        old_oddthreats = find_all_oddthreats(board=board)

        added_oddthreats = old_oddthreats - self.oddthreats
        removed_oddthreats = self.oddthreats - old_oddthreats

        self.oddthreats = old_oddthreats

        board.state[player][square.row][square.col] = 0

        return added_oddthreats, removed_oddthreats
