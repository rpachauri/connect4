from typing import List, Set

from connect_four.evaluation.victor.rules import Rule
from connect_four.game import Square
from connect_four.evaluation.victor.board import Board
from connect_four.problem import Group


class Baseclaim(Rule):
    def __init__(self, first: Square, second: Square, third: Square):
        """Initializes a Baseclaim instance.

        Args:
            first (Square): A directly playable Square. Left of the second square.
            second (Square): A directly playable odd Square.
            third (Square): A directly playable Square. Right of the second square.
        """
        self.first = first
        self.second = second
        self.third = third

    def __eq__(self, other):
        if isinstance(other, Baseclaim):
            return self.first == other.first and self.second == other.second and self.third == other.third
        return False

    def __hash__(self):
        return self.first.__hash__() * 41 + self.second.__hash__() * 31 + self.third.__hash__()

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
        white_problems_solved = self.find_problems_solved_for_player(groups_by_square=groups_by_square_by_player[0])
        black_problems_solved = self.find_problems_solved_for_player(groups_by_square=groups_by_square_by_player[1])
        return white_problems_solved.union(black_problems_solved)

    def find_problems_solved_for_player(self, groups_by_square: List[List[Set[Group]]]) -> Set[Group]:
        groups = set()

        # Add all groups which contain the first playable square and the square above the second playable square.
        square_above_second = Square(row=self.second.row - 1, col=self.second.col)
        groups.update(groups_by_square[self.first.row][self.first.col].intersection(
            groups_by_square[square_above_second.row][square_above_second.col]))

        # Add all groups which contain the second and third playable square.
        groups.update(groups_by_square[self.second.row][self.second.col].intersection(
            groups_by_square[self.third.row][self.third.col]))
        return groups


def find_all_baseclaims(board: Board):
    """find_all_baseclaims takes a Board and returns an iterable of Baseclaims for the Board.

    Args:
        board (Board): a Board instance.

    Returns:
        baseclaims (iterable<Baseclaim>): an iterable of Baseclaims for board.
    """
    baseclaims = set()
    playable_squares = board.playable_squares()

    for first in playable_squares:
        for second in playable_squares:
            if first == second or second.row % 2 == 0:
                continue
            for third in playable_squares:
                if third == first or third == second:
                    continue
                # if in_order(first, second, third):
                baseclaims.add(Baseclaim(first=first, second=second, third=third))
                baseclaims.add(Baseclaim(first=third, second=second, third=first))

    return baseclaims
