from typing import List, Set, FrozenSet

from connect_four.game import Square
from connect_four.problem import Group
from connect_four.problem import GroupDirection
from connect_four.evaluation.board import Board

from connect_four.evaluation.victor.rules import Claimeven, Rule
from connect_four.evaluation.victor.rules import Vertical

import warnings


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
        return self.group.__hash__() * 3593 + self.verticals.__hash__() * 9041 + self.claimevens.__hash__() * 3137

    def __repr__(self):
        return self.group.__repr__() + " Verticals: " + str(self.verticals) + " Claimevens: " + str(self.claimevens)

    def empty_squares_of_before_group(self) -> FrozenSet[Square]:
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

    def solves(self, group: Group) -> bool:
        if group.player == self.group.player:
            return False

        for claimeven in self.claimevens:
            if claimeven.solves(group=group):
                return True

        for vertical in self.verticals:
            if vertical.solves(group=group):
                return True

        return self.is_group_solvable_by_before(group=group)

    def is_useful(self, groups: Set[Group]) -> bool:
        for group in groups:
            if self.is_group_solvable_by_before(group=group):
                return True

        return False

    def is_group_solvable_by_before(self, group: Group) -> bool:
        """Returns whether or not group has at least one square in all Before columns,
        above the empty square of the Before group in that column.

        Args:
            group (Group): a Group to be solved.

        Returns:
            is_group_solvable_by_group (bool): true if this Before solves group; otherwise, false.
        """
        empty_squares_of_group = self.empty_squares_of_before_group()

        # For every empty square in the Before Group, group must contain its direct successor.
        for empty_square in empty_squares_of_group:
            square_above = Square(row=empty_square.row - 1, col=empty_square.col)
            if square_above not in group.squares:
                return False

        # If all empty squares of the Before Group is below a Square in group, return True.
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
        empty_squares = self.empty_squares_of_before_group()
        empty_square_successors = []
        for square in empty_squares:
            empty_square_successors.append(Square(row=square.row - 1, col=square.col))

        opponent = 1 - self.group.player

        before_groups = groups_by_square_by_player[opponent][
            empty_square_successors[0].row][empty_square_successors[0].col].copy()
        for square in empty_square_successors[1:]:
            before_groups.intersection_update(groups_by_square_by_player[opponent][square.row][square.col])

        for vertical in self.verticals:
            before_groups.update(vertical.find_problems_solved_for_player(
                groups_by_square=groups_by_square_by_player[opponent],
            ))

        for claimeven in self.claimevens:
            before_groups.update(claimeven.find_problems_solved_for_player(
                groups_by_square=groups_by_square_by_player[opponent],
            ))

        return before_groups


def find_all_befores(board: Board, opponent_groups) -> Set[Before]:
    """find_all_befores takes a Board and an iterable of Groups and returns an iterable of Befores for the Board.

    Args:
        board (Board): a Board instance.
        opponent_groups (iterable<Group>): an iterable of Groups belonging to the
            opponent of the player to move on board.

    Returns:
        befores (Set[Before]): an iterable of Befores for board.
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


def empty_squares_of_before_group(board: Board, group: Group) -> List[Square]:
    """Retrieves the empty squares of a Before group if the given group meets the conditions of a Before group.
    Returns an empty list if the group does not meet the conditions.

    Args:
        board (Board): a Board instance.
        group (Group): a possible Before group.

    Returns:
        empty_squares (List[Square]):
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


def add_before_variations(board: Board, befores: Set[Before], group: Group, empty_squares: List[Square],
                          verticals: List[Vertical], claimevens: List[Claimeven]):
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
        None.
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


class BeforeManager:
    def __init__(self, board: Board):
        """Initializes the BeforeManager.

        Args:
            board (Board): a Board instance.
        """
        self.befores = find_all_befores(board=board, opponent_groups=board.potential_groups(player=0))
        self.befores.update(find_all_befores(board=board, opponent_groups=board.potential_groups(player=1)))

    def move(self, player: int, square: Square, board: Board) -> (Set[Before], Set[Before]):
        """Moves the internal state of the BeforeManager to after this square has been played.

        Args:
            player (int): the player playing square.
            square (Square): the square being played.
            board (Board): the Board state, without square having been played yet.

        Returns:
            removed_befores (Set[Before]): the set of Befores being removed.
            added_befores (Set[Before]): the set of Befores being added.
        """
        removed_befores, added_befores = BeforeManager.added_removed_befores(player=player, square=square, board=board)

        self.befores.difference_update(removed_befores)
        self.befores.update(added_befores)

        return removed_befores, added_befores

    @staticmethod
    def added_removed_befores(player: int, square: Square, board: Board) -> (Set[Before], Set[Before]):
        """Finds the set of Befores that are added and removed after player would have played square in board.


        Requires:
            1. board.state[player][square.row][square.col] == 0

        Args:
            player (int): the player playing square.
            square (Square): the square being played.
            board (Board): the Board state, without square having been played yet.

        Returns:
            removed_befores (Set[Before]): the set of Befores being removed.
            added_befores (Set[Before]): the set of Befores being added.
        """
        removed_befores = set()

        removed_befores.update(BeforeManager._befores_containing_square_in_group(square=square, board=board))
        removed_befores.update(BeforeManager._befores_containing_square_outside_group(square=square, board=board))

        board.state[player][square.row][square.col] = 1
        added_befores = BeforeManager._befores_containing_square_in_group(square=square, board=board)
        board.state[player][square.row][square.col] = 0

        return removed_befores, added_befores

    @staticmethod
    def _befores_containing_square_in_group(square: Square, board: Board) -> Set[Before]:
        """Given a square, find all Befores that can be formed using square in the Before group.

        Args:
            square (Square): an empty Square. Every Before returned must have square in its Before group.
            board (Board):  a Board instance.

        Returns:
            befores (Set[Before]): a set of Befores, where each Before contains square in its Before group.
        """
        # Groups belonging to either player containing square.
        groups_containing_square = board.potential_groups_at_square(square)
        return find_all_befores(board, groups_containing_square)

    @staticmethod
    def _befores_containing_square_outside_group(square: Square, board: Board) -> Set[Before]:
        """Given a square, find all Befores that can be formed using square as the lower square of a Vertical or
        Claimeven. The square must not be part of the Before group.

        Args:
            square (Square): an empty Square.
            board: a Board instance.

        Returns:
            befores (Set[Before]): a set of Befores, where each Before contains square as the lower square of one of
                its Verticals or Claimevens. The square must not be part of the Before group.
        """
        # If the square is in the top row, there are no new Befores.
        if square.row == 0:
            return set()

        # Find all Befores that contain above in the Before group.
        above = Square(row=square.row - 1, col=square.col)
        befores_containing_above_in_group = BeforeManager._befores_containing_square_in_group(square=above, board=board)

        # Of those Befores, find the subset that contains square.
        befores = set()
        for before in befores_containing_above_in_group:
            if BeforeManager._square_lower_in_before_outside_group(square=square, before=before):
                befores.add(before)

        return befores

    @staticmethod
    def _square_lower_in_before_outside_group(square: Square, before: Before) -> bool:
        """Returns whether or not the given square is the lower square of one of the Verticals or Claimevens in before.

        Args:
            square (Square): a Square.
            before (Before): a Before, whose Before group contains the square above square.

        Returns:
            in (bool): True if square is the lower square of one of before's Verticals or Claimevens. Otherwise, false.
        """
        for vertical in before.verticals:
            if square == vertical.lower:
                return True
        for claimeven in before.claimevens:
            if square == claimeven.lower:
                return True

        return False

    def undo_move(self, player: int, square: Square, board: Board) -> (Set[Before], Set[Before]):
        """Moves the internal state of the BeforeManager to before this square was played.

        Args:
            player (int): the player who had square.
            square (Square): the square being undone.
            board (Board): the Board state, with square being empty.

        Returns:
            added_befores (Set[Before]): the set of Befores being added.
            removed_befores (Set[Before]): the set of Befores being removed.
        """
        added_befores, removed_befores = BeforeManager.added_removed_befores(player=player, square=square, board=board)

        self.befores.update(added_befores)
        self.befores.difference_update(removed_befores)

        return added_befores, removed_befores
