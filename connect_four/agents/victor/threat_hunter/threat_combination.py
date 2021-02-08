from collections import namedtuple
from enum import Enum
from typing import Optional, Set

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Group
from connect_four.agents.victor.game import Square


class ThreatCombinationType(Enum):
    EvenAboveOdd = 0
    OddAboveNotDirectlyPlayableEven = 1
    OddAboveDirectlyPlayableEven = 2


EvenGroup = namedtuple("EvenGroup", ["group", "odd_square", "even_square"])
OddGroup = namedtuple("OddGroup", ["group", "odd_square1", "odd_square2"])


class ThreatCombination:
    """A ThreatCombination is a combination of two threats.

    Both threats have exactly two squares filled by the player and two empty squares.

    From Section 8.4 of the original paper:

        A threat_hunter combination consists of two threats, which both are filled with two [tokens]. One threat_hunter needs two odd
        squares, while the second threat_hunter needs one of the two squares of the first threat_hunter, and another even square, directly
        above, or beneath the second odd square of the first threat_hunter. The square which both threats share should not be
        directly playable.

    Naming:
    -   The threat_hunter with the even empty square (not the shared one) is known as the "even threat_hunter".
    -   The threat_hunter with the odd empty square (not the shared one) is known as the "odd threat_hunter".
    -   Despite the naming, either can be used as an odd threat_hunter depending on the opponent's moves.
    """
    def __init__(self,
                 even_threat: Group,
                 odd_threat: Group,
                 shared_square: Square,
                 even_square: Square,
                 odd_square: Square,
                 threat_combination_type: ThreatCombinationType):
        self.even_threat = even_threat
        self.odd_threat = odd_threat
        self.shared_square = shared_square
        self.even_square = even_square
        self.odd_square = odd_square
        self.threat_combination_type = threat_combination_type

    def __eq__(self, other):
        if isinstance(other, ThreatCombination):
            return (self.even_threat == other.even_threat and
                    self.odd_threat == other.odd_threat and
                    self.shared_square == other.shared_square and
                    self.even_square == other.even_square and
                    self.odd_square == other.odd_square and
                    self.threat_combination_type == other.threat_combination_type)

    def crossing_column(self) -> int:
        return self.shared_square.col

    def stacked_column(self) -> int:
        return self.even_square.col

    def upper_square_in_stacked_column(self) -> Square:
        if self.threat_combination_type == ThreatCombinationType.EvenAboveOdd:
            return self.even_square
        return self.odd_square


def find_threat_combination(board: Board):
    """find_threat_combination returns a ThreatCombination for White if one exists. Otherwise, returns None.
    If multiple threatCombinations exist, picks one arbitrarily.

    Args:
        board (Board): a Board instance.

    Returns:
        threat_combination (ThreatCombination): a ThreatCombination for White if one exists. Otherwise, None.
    """
    white_groups = board.potential_groups(0)

    even_threats = []
    odd_threats = []
    for group in white_groups:
        empty_squares = []
        for square in group.squares:
            if board.is_empty(square):
                empty_squares.append(square)

        if len(empty_squares) != 2:
            continue

        square1, square2 = empty_squares[0], empty_squares[1]
        if square1.row % 2 == 1 and square2.row % 2 == 1:  # odd threat_hunter.
            odd_threats.append(OddGroup(group=group, odd_square1=square1, odd_square2=square2))
        elif square1.row % 2 == 0 and square2.row % 2 == 1:  # even threat_hunter with square1 as the even square.
            even_threats.append(EvenGroup(group=group, odd_square=square2, even_square=square1))
        elif square1.row % 2 == 1 and square2.row % 2 == 0:  # even threat_hunter with square2 as the even square.
            even_threats.append(EvenGroup(group=group, odd_square=square1, even_square=square2))

    directly_playable_squares = board.playable_squares()
    for even_threat in even_threats:
        for odd_threat in odd_threats:
            threat_combination = create_threat_combination(
                even_threat=even_threat,
                odd_threat=odd_threat,
                directly_playable_squares=directly_playable_squares,
            )
            if threat_combination:
                return threat_combination


def create_threat_combination(
        even_threat: EvenGroup,
        odd_threat: OddGroup,
        directly_playable_squares: Set[Square]) -> Optional[ThreatCombination]:
    odd_unshared_square = shared_square(even_threat=even_threat, odd_threat=odd_threat)
    if odd_unshared_square is None:
        return None
    if even_threat.even_square.col != odd_unshared_square.col:
        return None

    if even_threat.even_square.row - odd_unshared_square.row == -1:
        threat_combination_type = ThreatCombinationType.EvenAboveOdd
    elif even_threat.even_square.row - odd_unshared_square.row == 1:
        if even_threat.even_square in directly_playable_squares:
            threat_combination_type = ThreatCombinationType.OddAboveDirectlyPlayableEven
        else:
            threat_combination_type = ThreatCombinationType.OddAboveNotDirectlyPlayableEven
    else:
        return None

    return ThreatCombination(
        even_threat=even_threat.group,
        odd_threat=odd_threat.group,
        shared_square=even_threat.odd_square,
        even_square=even_threat.even_square,
        odd_square=odd_unshared_square,
        threat_combination_type=threat_combination_type,
    )


def shared_square(even_threat: EvenGroup, odd_threat: OddGroup) -> Square:
    if even_threat.odd_square == odd_threat.odd_square1:
        return odd_threat.odd_square2
    if even_threat.odd_square == odd_threat.odd_square2:
        return odd_threat.odd_square1
