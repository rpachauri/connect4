from typing import List, Set

from connect_four.game import Square
from connect_four.evaluation.victor.board import Board

from connect_four.evaluation.victor.rules import Vertical, Rule
from connect_four.evaluation.victor.rules import Before
from connect_four.problem import Group


class Specialbefore(Rule):
    def __init__(self,
                 before: Before,
                 internal_directly_playable_square: Square,
                 external_directly_playable_square: Square):
        """Initializes a Specialbefore instance.

        Assumptions:
            1. The internal directly playable square belongs to at most one Vertical.
                a. This allows us to not have to dedupe different variations of Befores.
                b. Note that this is important because that Vertical does not get used by the Specialbefore.
            2. A requirement of the Before is that there must be at least one Vertical. This is not a
                requirement of the Specialbefore.

        Args:
            before (Before): A Before. At least one empty square of the Before group must be playable.
            internal_directly_playable_square (Square): A directly playable square part of the Before group.
            external_directly_playable_square (Square): A directly playable square not part of the Before group.
        """
        # An assumption we make is that the internal directly playable square belongs to at most one Vertical.
        # This allows us to not have to dedupe different variations of Befores.
        # Note that this is important because that Vertical does not get used by the Specialbefore.
        # Also note that a requirement of the Before is that there must be at least one Vertical. This is not a
        # requirement of the Specialbefore.
        self.before = before
        self.internal_directly_playable_square = internal_directly_playable_square
        self.external_directly_playable_square = external_directly_playable_square

    def __eq__(self, other):
        if isinstance(other, Specialbefore):
            return (self.before == other.before and
                    self.internal_directly_playable_square == other.internal_directly_playable_square and
                    self.external_directly_playable_square == other.external_directly_playable_square)
        return False

    def __hash__(self):
        return (self.before.__hash__() * 59 +
                self.internal_directly_playable_square.__hash__() * 47 +
                self.external_directly_playable_square.__hash__())

    def unused_vertical(self) -> Vertical:
        """
        Returns:
            unused_vertical (Vertical): a Vertical part of the Before but not part of the Specialbefore.
                The lower square of the Vertical is the internal directly playable square of the Specialbefore.
        """
        return Vertical(
            lower=self.internal_directly_playable_square,
            upper=Square(
                row=self.internal_directly_playable_square.row - 1,
                col=self.internal_directly_playable_square.col,
            ),
        )

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
        opponent = 1 - self.before.group.player
        # Find all groups that contain the external directly playable square and
        # all successors of empty squares of the Specialbefore.
        external_and_successor_groups = groups_by_square_by_player[opponent][
            self.external_directly_playable_square.row][self.external_directly_playable_square.col]
        empty_squares = self.before.empty_squares_of_before_group()
        for square in empty_squares:
            direct_successor = Square(row=square.row - 1, col=square.col)
            external_and_successor_groups = external_and_successor_groups.intersection(
                groups_by_square_by_player[opponent][direct_successor.row][direct_successor.col])

        # Find all groups that contain the internal directly playable square and
        # external directly playable square of the Specialbefore.
        # Essentially, reproducing the groups refuted by a Baseinverse.
        sq1 = self.internal_directly_playable_square
        sq2 = self.external_directly_playable_square
        directly_playable_squares_groups = groups_by_square_by_player[opponent][sq1.row][sq1.col].intersection(
            groups_by_square_by_player[opponent][sq2.row][sq2.col])

        groups = external_and_successor_groups.union(directly_playable_squares_groups)

        for vertical in self.before.verticals:
            if vertical != self.unused_vertical():
                # Add all groups refuted by Verticals which are part of the Before.
                groups.update(vertical.find_problems_solved_for_player(
                    groups_by_square=groups_by_square_by_player[opponent],
                ))

        for claimeven in self.before.claimevens:
            # Add all groups refuted by Claimevens which are part of the Before.
            groups.update(claimeven.find_problems_solved_for_player(
                groups_by_square=groups_by_square_by_player[opponent],
            ))

        return groups


def find_all_specialbefores(board: Board, befores):
    """find_all_specialbefores takes a Board and an iterable of Befores for the Board and
    outputs an iterable of Specialbefores for the Board.

    Args:
        board (Board): a Board instance
        befores (iterable<Before>): an iterable of Befores for board.

    Returns:
        specialbefores (iterable<Specialbefore>): an iterable of Specialbefores for board.
    """
    specialbefores = set()
    directly_playable_squares = board.playable_squares()

    for before in befores:
        directly_playable_squares_in_before_group = internal_directly_playable_squares(
            before, directly_playable_squares)
        for internal_directly_playable_square in directly_playable_squares_in_before_group:
            for external_directly_playable_square in directly_playable_squares:
                if can_be_used_with_before(external_directly_playable_square, before):
                    specialbefores.add(Specialbefore(
                        before=before,
                        internal_directly_playable_square=internal_directly_playable_square,
                        external_directly_playable_square=external_directly_playable_square,
                    ))

    return specialbefores


def internal_directly_playable_squares(before: Before, directly_playable_squares):
    """Returns a set of directly playable squares in before.group.squares.
    If there are none, returns an empty set.

    Args:
        before (Before): a Before.
        directly_playable_squares (iterable<Square>): an iterable of directly playable squares.

    Returns:
        squares (Set<Square>): a Set of all Squares that exist in both
            before.group.squares and directly_playable_squares.
    """
    return before.group.squares.intersection(directly_playable_squares)


def can_be_used_with_before(external_directly_playable_square: Square, before: Before):
    # A requirement of the Specialbefore is that the directly playable square
    # must not be a part of the Before.
    # A weaker condition is that the directly playable square does not belong in the same
    # column as any empty square of the Before.
    for square in before.empty_squares_of_before_group():
        if external_directly_playable_square.col == square.col:
            return False
    return True
