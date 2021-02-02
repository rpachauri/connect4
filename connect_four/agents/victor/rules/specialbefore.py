from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Before


class Specialbefore:
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
            internal_directly_playable_square (Square): A directly playable square part of the Before.
            external_directly_playable_square (Square): A directly playable square not part of the Before.
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
                if external_directly_playable_square not in directly_playable_squares_in_before_group:
                    # Recall that a requirement of the Specialbefore is that the directly playable square
                    # must not be a part of the Before.
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
