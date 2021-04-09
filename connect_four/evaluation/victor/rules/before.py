from typing import List, Set

from connect_four.game import Square
from connect_four.problem import Group
from connect_four.problem import GroupDirection
from connect_four.evaluation.victor.board import Board

from connect_four.evaluation.victor.rules import Claimeven, Rule
from connect_four.evaluation.victor.rules import Vertical


class Before(Rule):
    def __init__(self, group: Group, verticals, claimevens):
        """Initializes a Before instance.

        Args:
            group (Group): a group representing the Before group.
            verticals (iterable<Vertical>): an iterable of Verticals which are part of the Before.
            claimevens (iterable<Vertical>): an iterable of Claimevens which are part of the Before.
        """
        self.group = group
        self.verticals = frozenset(verticals)
        self.claimevens = frozenset(claimevens)

    def __eq__(self, other):
        if isinstance(other, Before):
            return (self.group == other.group and
                    self.verticals == other.verticals and
                    self.claimevens == other.claimevens)

    def __hash__(self):
        return self.group.__hash__() * 41 + self.verticals.__hash__() * 31 + self.claimevens.__hash__()

    def empty_squares_of_before_group(self):
        """Returns the empty squares of the Before group of this Before.

        Returns:
            empty_squares (Set<Square>): The empty squares of the Before group of this Before.
        """
        empty_squares = set()

        for vertical in self.verticals:
            if vertical.upper in self.group.squares:
                empty_squares.add(vertical.upper)
            else:
                empty_squares.add(vertical.lower)

        for claimeven in self.claimevens:
            # claimeven.upper should be an empty square part of the Before group by definition.
            # Otherwise, something is wrong.
            empty_squares.add(claimeven.upper)

        return frozenset(empty_squares)

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
        pass


def find_all_befores(board: Board, opponent_groups):
    """find_all_befores takes a Board and an iterable of Groups and returns an iterable of Befores for the Board.

    Args:
        board (Board): a Board instance.
        opponent_groups (iterable<Group>): an iterable of Groups belonging to the
            opponent of the player to move on board.

    Returns:
        befores (iterable<Before>): an iterable of Befores for board.
    """
    befores = set()

    for group in opponent_groups:
        # Skip all Vertical Groups.
        if group.direction == GroupDirection.vertical:
            continue

        # empty_squares is the set of all squares that belong to group and are empty.
        # If there is a single square that belongs in the uppermost row of board, then len(empty_squares) == 0.
        empty_squares = empty_squares_of_before_group(board, group)

        if empty_squares:  # Only create variations if empty_squares has at least one square.
            # Add all Before variations with group as the Before group to befores.
            add_before_variations(board, befores, group, empty_squares, [], [])

    return befores


def empty_squares_of_before_group(board: Board, group: Group):
    """Retrieves the empty squares of a Before group if the given group meets the conditions of a Before group.
    Returns an empty list if the group does not meet the conditions.

    Args:
        board (Board): a Board instance.
        group (Group): a possible Before group.

    Returns:
        empty_squares (list<Square>):
            If there exists an empty square with square.row == 0 in group:
                returns []
            Otherwise:
                returns a list of empty Squares in group.
    """
    empty_squares = []
    for square in group.squares:
        if board.is_empty(square):
            if square.row == 0:
                return []
            empty_squares.append(square)
    return empty_squares


def add_before_variations(board: Board, befores, group: Group, empty_squares, verticals, claimevens):
    """Adds all Before variations with group as the Before group to befores.

    Args:
        board (Board): a Board instance.
        befores (set<Before>): a set of Befores we have accumulated so far for board.
            Any new Befores we find with group as the Before group will be added to befores.
        group (Group): the Before group. Any new Befores we add to befores must use group as their Before group.
        empty_squares (list<Square>): a list of empty Squares in group.
        verticals (set<Vertical>): a set of Verticals which are part of the Before we are building.
        claimevens (set<Claimeven>): a set of Claimevens which are part of the Before we are building.

    Returns:

    """
    # This is a Recursive Backtracking algorithm.
    # Base Case.
    if not empty_squares:
        if len(verticals) > 0:
            # Only add the Before if there is at least one Vertical; otherwise, an Aftereven is better.
            befores.add(Before(group=group, verticals=verticals, claimevens=claimevens))
        return

    # Recursive Case.
    square = empty_squares.pop()  # Remove a square from empty_squares.
    square_below = Square(row=square.row + 1, col=square.col)
    square_above = Square(row=square.row - 1, col=square.col)

    # Whether square is odd or even, we can always try to create a Vertical with square as the lower square.
    if board.is_valid(square_above):
        vertical = Vertical(upper=square_above, lower=square)
        # Choose.
        verticals.append(vertical)
        # Recurse.
        add_before_variations(board, befores, group, empty_squares, verticals, claimevens)
        # Unchoose.
        verticals.remove(vertical)

    # Depending on whether square is odd or even, we try to create a Vertical or Claimeven respectively.
    if square.row % 2 == 1:  # square is odd.
        if board.is_valid(square_below) and board.is_empty(square_below):
            # Create a Vertical with square as the upper square.
            vertical = Vertical(upper=square, lower=square_below)
            # Choose.
            verticals.append(vertical)
            # Recurse.
            add_before_variations(board, befores, group, empty_squares, verticals, claimevens)
            # Unchoose.
            verticals.remove(vertical)
    else:  # square is even.
        # Since square is even, we are guaranteed that square_below is valid
        # because board must have an even number of rows.
        if board.is_empty(square_below):
            # Create a Claimeven with square as the upper square.
            claimeven = Claimeven(upper=square, lower=square_below)
            # Choose.
            claimevens.append(claimeven)
            # Recurse.
            add_before_variations(board, befores, group, empty_squares, verticals, claimevens)
            # Unchoose.
            claimevens.remove(claimeven)

    empty_squares.append(square)
