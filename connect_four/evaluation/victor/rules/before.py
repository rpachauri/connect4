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

    def __repr__(self):
        return self.group.__repr__() + " Verticals: " + str(self.verticals) + " Claimevens: " + str(self.claimevens)

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
            removed_befores (Set[Before]): the set of Afterevens being removed.
            added_befores (Set[Before]): the set of Afterevens being added.
        """
        pass

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
        pass

    def undo_move(self, player: int, square: Square, board: Board) -> (Set[Before], Set[Before]):
        """Moves the internal state of the BeforeManager to before this square was played.

        Args:
            player (int): the player who had square.
            square (Square): the square being undone.
            board (Board): the Board state, with square being empty.

        Returns:
            added_befores (Set[Before]): the set of Afterevens being added.
            removed_befores (Set[Before]): the set of Afterevens being removed.
        """
        pass
