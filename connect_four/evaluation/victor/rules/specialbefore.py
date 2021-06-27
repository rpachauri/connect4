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


def find_all_specialbefores(board: Board, befores) -> Set[Specialbefore]:
    """find_all_specialbefores takes a Board and an iterable of Befores for the Board and
    outputs an iterable of Specialbefores for the Board.

    Args:
        board (Board): a Board instance
        befores (iterable<Before>): an iterable of Befores for board.

    Returns:
        specialbefores (iterable<Specialbefore>): an iterable of Specialbefores for board.
    """
    directly_playable_squares = board.playable_squares()
    return find_all_specialbefores_with_playable_squares(
        befores=befores,
        directly_playable_squares=directly_playable_squares,
    )


def find_all_specialbefores_with_playable_squares(
        befores: Set[Before], directly_playable_squares: Set[Square]) -> Set[Specialbefore]:
    specialbefores = set()
    for external_directly_playable_square in directly_playable_squares:
        specialbefores.update(specialbefores_given_external_square(
            befores=befores,
            directly_playable_squares=directly_playable_squares,
            external_directly_playable_square=external_directly_playable_square,
        ))

    return specialbefores


def specialbefores_given_external_square(
        befores: Set[Before],
        directly_playable_squares: Set[Square],
        external_directly_playable_square: Square) -> Set[Specialbefore]:
    """

    Args:
        befores (Set[Before]): a set of Befores used to create Specialbefores.
        directly_playable_squares (Set[Square]): a set of directly playable squares, possibly including square.
        external_directly_playable_square (Square): a square to be used as the external directly playable
            square of each Specialbefore.

    Returns:
        specialbefores (Set[Specialbefore]): a set of Specialbefores. Each Specialbefore uses square as its external
            directly playable square.
    """
    specialbefores = set()
    for before in befores:
        directly_playable_squares_in_before_group = internal_directly_playable_squares(
            before, directly_playable_squares)
        for internal_directly_playable_square in directly_playable_squares_in_before_group:
            if can_be_used_with_before(external_directly_playable_square, before):
                specialbefores.add(Specialbefore(
                    before=before,
                    internal_directly_playable_square=internal_directly_playable_square,
                    external_directly_playable_square=external_directly_playable_square,
                ))
    return specialbefores


def specialbefores_given_internal_square(
        befores: Set[Before],
        directly_playable_squares: Set[Square],
        internal_directly_playable_square: Square) -> Set[Specialbefore]:
    """

    Args:
        befores (Set[Before]): a set of Befores used to create Specialbefores.
        directly_playable_squares (Set[Square]): a set of directly playable squares, possibly including square.
        internal_directly_playable_square (Square): a square to be used as the internal directly playable
            square of each Specialbefore.

    Returns:
        specialbefores (Set[Specialbefore]): a set of Specialbefores. Each Specialbefore uses square as its external
            directly playable square.
    """
    specialbefores = set()
    for before in befores:
        if internal_directly_playable_square in before.group.squares:
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


class SpecialbeforeManager:
    def __init__(self, board: Board, befores: Set[Before]):
        self.specialbefores = find_all_specialbefores(board=board, befores=befores)

    def move(self, square: Square, board: Board, removed_befores: Set[Before],
             added_befores: Set[Before], befores: Set[Before]) -> (Set[Specialbefore], Set[Specialbefore]):
        """Moves the internal state of the SpecialbeforeManager to after this square has been played.

        Args:
            square (Square): the Square being played.
            board (Board): a Board instance. square has not been played yet.
            removed_befores (Set[Specialbefore]): the set of Befores removed after square is played.
            added_befores (Set[Specialbefore]): the set of Befores added after square is played.
            befores (Set[Specialbefore]): the intersection between the set of Befores before and after this move is undone.

        Returns:
            removed_specialbefores (Set[Specialbefore]): the set of Specialbefores removed after square is played.
            added_specialbefores (Set[Specialbefore]): the set of Specialbefores added after square is played.
        """
        removed_specialbefores, added_specialbefores = SpecialbeforeManager.added_removed_specialbefores(
            square=square,
            board=board,
            removed_befores=removed_befores,
            added_befores=added_befores,
            befores=befores,
        )

        self.specialbefores.difference_update(removed_specialbefores)
        self.specialbefores.update(added_specialbefores)

        return removed_specialbefores, added_specialbefores

    @staticmethod
    def added_removed_specialbefores(
            square: Square, board: Board, removed_befores: Set[Before],
            added_befores: Set[Before], befores: Set[Before]) -> (Set[Specialbefore], Set[Specialbefore]):
        removed_specialbefores = set()
        added_specialbefores = set()

        directly_playable_squares = board.playable_squares()
        new_directly_playable_squares = directly_playable_squares.difference({square})

        if square.row > 0:
            above = Square(row=square.row - 1, col=square.col)
            new_directly_playable_squares.update({above})

            added_specialbefores.update(specialbefores_given_external_square(
                befores=befores,
                directly_playable_squares=new_directly_playable_squares,
                external_directly_playable_square=above,
            ))

            added_specialbefores.update(specialbefores_given_internal_square(
                befores=befores,
                directly_playable_squares=new_directly_playable_squares,
                internal_directly_playable_square=above,
            ))

        removed_specialbefores.update(find_all_specialbefores(board=board, befores=removed_befores))
        added_specialbefores.update(find_all_specialbefores_with_playable_squares(
            befores=added_befores,
            directly_playable_squares=new_directly_playable_squares,
        ))

        removed_specialbefores.update(specialbefores_given_external_square(
            befores=befores,
            directly_playable_squares=directly_playable_squares,
            external_directly_playable_square=square,
        ))

        return removed_specialbefores, added_specialbefores

    def undo_move(self, square: Square, board: Board, added_befores: Set[Before],
                  removed_befores: Set[Before], befores: Set[Before]) -> (Set[Specialbefore], Set[Specialbefore]):
        """Moves the internal state of the SpecialbeforeManager to after this square has been played.

        Args:
            square (Square): the Square being undone.
            board (Board): a Board instance. square has already been undone.
            added_befores (Set[Before]): the set of Befores added after square is undone.
            removed_befores (Set[Before]): the set of Befores removed after square is undone.
            befores (Set[Before]): the intersection between the set of Befores before and after this move is undone.

        Returns:
            added_specialbefores (Set[Specialbefore]): the set of Specialbefores added after square is played.
            removed_specialbefores (Set[Specialbefore]): the set of Specialbefores removed after square is played.
        """
        added_specialbefores, removed_specialbefores = SpecialbeforeManager.added_removed_specialbefores(
            square=square,
            board=board,
            removed_befores=added_befores,
            added_befores=removed_befores,
            befores=befores,
        )

        self.specialbefores.update(added_specialbefores)
        self.specialbefores.difference_update(removed_specialbefores)

        return added_specialbefores, removed_specialbefores
