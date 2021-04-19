from typing import List, Set

from connect_four.evaluation.victor.rules import Rule, Claimeven
from connect_four.game import Square
from connect_four.problem import Group
from connect_four.evaluation.victor.board import Board


class Aftereven(Rule):
    def __init__(self, group: Group, claimevens):
        """Initializes an Aftereven instance.

        Args:
            group (Group): a group representing the Aftereven group.
            claimevens (iterable<Claimeven>): an iterable of Claimevens which are part of the Aftereven.
        """
        self.group = group
        self.claimevens = frozenset(claimevens)

    def __eq__(self, other):
        if isinstance(other, Aftereven):
            return self.group == other.group and self.claimevens == other.claimevens
        return False

    def __hash__(self):
        return self.group.__hash__() * 31 + self.claimevens.__hash__()

    def empty_squares_of_aftereven_group(self):
        empty_squares = []

        for claimeven in self.claimevens:
            # claimeven.upper should be an empty square part of the Aftereven group by definition.
            # Otherwise, something is wrong.
            empty_squares.append(claimeven.upper)

        return empty_squares

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
        groups = set()
        self.add_new_groups_from_aftereven(
            groups=groups,
            empty_squares_of_aftereven=self.empty_squares_of_aftereven_group(),
            threatening_squares=[],
            groups_by_square=groups_by_square_by_player[1 - self.group.player],
        )
        for claimeven in self.claimevens:
            groups.update(claimeven.find_problems_solved_for_player(
                groups_by_square=groups_by_square_by_player[1 - self.group.player],
            ))
        return groups

    @staticmethod
    def add_new_groups_from_aftereven(
            groups: Set[Group],
            empty_squares_of_aftereven: List[Square],
            threatening_squares: List[Square],
            groups_by_square: List[List[Set[Group]]]):
        """Adds any new groups that intersect squares above empty_squares_of_aftereven to groups.
        This is a recursive backtracking algorithm.
        threatening_squares starts out as an empty list.
        empty_squares_of_aftereven starts out as a list of all empty squares of the aftereven.

        We select a square from empty_squares_of_aftereven and remove it from the list.
        For every square above that square, we add it to threatening_squares, recurse, and then remove it from
          threatening_squares.
        The base case is when empty_squares_of_aftereven is empty. At that point, we find all groups that include
          all squares in threatening_squares and add them to groups.

        Args:
            groups (Set[Group]): a Set of groups this function will add to.
            empty_squares_of_aftereven (List[Square]):
                A subset of empty Squares that belong to an Aftereven.
                If two Squares from the Aftereven belong in the same column,
                    the Square from the higher row should be given.
                It is required that none of the Squares share the same column.
            threatening_squares (List[Square]):
                A list of Squares that could belong to a group that the Aftereven refutes.
                It is required that none of the Squares share the same column.
            groups_by_square (List[List[Set[Group]]]): A 2D array mapping each
                Square to all groups that contain that Square.

        Returns:
            None
        """
        # Base case.
        if not empty_squares_of_aftereven:
            new_groups_to_add = groups_by_square[threatening_squares[0].row][threatening_squares[0].col]
            for square in threatening_squares[1:]:
                new_groups_to_add = new_groups_to_add.intersection(groups_by_square[square.row][square.col])
            groups.update(new_groups_to_add)
            return

        # Recursive Case.
        square = empty_squares_of_aftereven.pop()
        for row in range(square.row - 1, -1, -1):
            square_above = Square(row=row, col=square.col)
            # Choose.
            threatening_squares.append(square_above)
            # Recurse.
            Aftereven.add_new_groups_from_aftereven(
                groups, empty_squares_of_aftereven, threatening_squares, groups_by_square)
            # Unchoose.
            threatening_squares.remove(square_above)
        empty_squares_of_aftereven.append(square)


def find_all_afterevens(board: Board, opponent_groups) -> Set[Aftereven]:
    """find_all_afterevens takes a Board and a set of Claimevens and returns a set of Afterevens for the Board.

    Args:
        board (Board): a Board instance.
        opponent_groups (iterable<Group>): an iterable of Groups belonging to the
            opponent of the player to move on board.

    Returns:
        afterevens (set<Aftereven>): a set of Afterevens for board.
    """
    afterevens = set()
    for group in opponent_groups:
        aftereven_claimevens = get_aftereven_claimevens(board, group)
        if aftereven_claimevens is not None:
            afterevens.add(Aftereven(group, aftereven_claimevens))

    return afterevens


def get_aftereven_claimevens(board: Board, group: Group):
    """get_aftereven_claimevens takes a Board, set of Claimevens and a group.
    It figures out if the group is an Aftereven group.
    If the group is an Aftereven group, then it returns the Claimevens which are part of the Aftereven.
    If the group is not an Aftereven group, then it returns None.

    Args:
        board (Board): a Board instance.
        group (Group): a group on this board.

    Returns:
        claimevens (iterable<Claimeven>):
            If the given group is an Aftereven group, an iterable of Claimevens,
            where the upper square of each Claimeven is an empty square in the Aftereven group.

            If the given group is not an Aftereven group, returns None.
    """
    claimevens = set()

    for square in group.squares:
        # If the square is not empty, we assume it already belongs to the player who owns the Group.
        if board.is_empty(square):
            # If a square is in the top row, then this would be a useless Aftereven.
            if square.row == 0:
                return None

            # If square is odd, then we cannot use a Claimeven to build the Aftereven.
            if square.row % 2 == 1:
                return None

            lower = Square(row=square.row + 1, col=square.col)

            # If an even square of an Aftereven group is empty, but the square below it is not,
            # then it is not a Claimeven.
            if not board.is_valid(square=lower) or not board.is_empty(square=lower):
                return None

            claimevens.add(Claimeven(lower=lower, upper=square))

    return claimevens
