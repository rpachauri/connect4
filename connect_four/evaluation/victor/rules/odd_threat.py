from typing import List, Set

from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.rules import Rule
from connect_four.game import Square
from connect_four.problem import Group


class OddThreat(Rule):
    def __init__(self, group: Group, empty_square: Square, directly_playable_square: Square):
        self.group = group
        self.empty_square = empty_square
        self.directly_playable_square = directly_playable_square

    def __eq__(self, other):
        if isinstance(other, OddThreat):
            return self.group == other.group and self.empty_square == other.empty_square
        return False

    def __hash__(self):
        return self.group.__hash__() * 97 + self.empty_square.__hash__() * 31

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
        problems_solved = set()

        # Add Groups containing any odd Square up to the Odd Threat that are not directly playable.
        for row in range(self.empty_square.row, self.directly_playable_square.row, 2):
            problems_solved.update(groups_by_square_by_player[1][row][self.empty_square.col])

        # Add Groups containing any Squares above the odd Threat.
        for row in range(0, self.empty_square.row, 1):
            problems_solved.update(groups_by_square_by_player[1][row][self.empty_square.col])

        # noinspection PyTypeChecker
        return problems_solved


def find_all_odd_threats(board: Board) -> Set[OddThreat]:
    """find_threat_combination returns an Odd Threat for White if one exists. Otherwise, returns None.
    If multiple Odd Threats exist, picks one arbitrarily.

    Args:
        board (Board): a Board instance.

    Returns:
        odd_group (Threat): a Threat with a single empty square. The single empty square will be odd.
            None if no such Threat exists for board.
    """
    directly_playable_squares = board.playable_squares()
    # Iterate through all groups that belong to White.
    odd_threats = set()
    for group in board.potential_groups(player=0):
        empty_squares = empty_squares_of_group(board, group)
        # If there is only 1 empty square in the group, the square is not directly playable, and it is an odd square:
        if (len(empty_squares) == 1 and
                empty_squares[0] not in directly_playable_squares and
                empty_squares[0].col % 2 == 1):
            empty_square = empty_squares[0]
            odd_threat = OddThreat(
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
