from collections import namedtuple
from enum import Enum
from typing import Optional, Set, List

from connect_four.evaluation.victor.rules import Rule, Vertical, Baseinverse, Claimeven
from connect_four.game import Square
from connect_four.problem import Group
from connect_four.evaluation.victor.board import Board


class ThreatCombinationType(Enum):
    EvenAboveOdd = 0
    OddAboveNotDirectlyPlayableEven = 1
    OddAboveDirectlyPlayableEven = 2


EvenGroup = namedtuple("EvenGroup", ["group", "odd_square", "even_square"])
OddGroup = namedtuple("OddGroup", ["group", "odd_square1", "odd_square2"])


# noinspection PyTypeChecker
class ThreatCombination(Rule):
    """A ThreatCombination is a combination of two threats.

    Both threats have exactly two squares filled by the player and two empty squares.

    From Section 8.4 of the original paper:

        A ThreatCombination consists of two Groups, which both are filled with two [tokens].
        One Group needs two odd squares, while the second Group needs one of the two squares of the
        first Group, and another even square, directly above, or beneath the second odd square of the first Group.
        The square which both Groups share should not be directly playable.

    Naming:
    -   The Group with the even empty square (not the shared one) is known as the "even group".
    -   The Group with the odd empty square (not the shared one) is known as the "odd group".
    -   Despite the naming, either can be used as an odd threat depending on the opponent's moves.
    """
    def __init__(self,
                 even_group: Group,
                 odd_group: Group,
                 shared_square: Square,
                 even_square: Square,
                 odd_square: Square,
                 directly_playable_square_shared_col: Square,
                 directly_playable_square_stacked_col: Square,
                 threat_combination_type: ThreatCombinationType):
        self.even_threat = even_group
        self.odd_threat = odd_group
        self.shared_square = shared_square
        self.even_square = even_square
        self.odd_square = odd_square
        self.directly_playable_square_shared_col = directly_playable_square_shared_col
        self.directly_playable_square_stacked_col = directly_playable_square_stacked_col
        self.threat_combination_type = threat_combination_type

    def __eq__(self, other):
        if isinstance(other, ThreatCombination):
            return (self.even_threat == other.even_threat and
                    self.odd_threat == other.odd_threat and
                    self.shared_square == other.shared_square and
                    self.even_square == other.even_square and
                    self.odd_square == other.odd_square and
                    self.directly_playable_square_shared_col == other.directly_playable_square_shared_col and
                    self.directly_playable_square_stacked_col == other.directly_playable_square_stacked_col and
                    self.threat_combination_type == other.threat_combination_type)

    def __hash__(self):
        return (self.even_threat.__hash__() * 97 +
                self.odd_threat.__hash__() * 89 +
                self.shared_square.__hash__() * 79 +
                self.even_square.__hash__() * 73 +
                self.odd_square.__hash__() * 71)

    def upper_square_in_stacked_column(self) -> Square:
        if self.threat_combination_type == ThreatCombinationType.EvenAboveOdd:
            return self.even_square
        return self.odd_square

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
        problems_solved.update(self._no_odd_squares_in_crossing_column(groups_by_square=groups_by_square_by_player[1]))
        problems_solved.update(self._no_squares_above_crossing_and_above_odd(
            groups_by_square=groups_by_square_by_player[1],
        ))
        problems_solved.update(self._groups_containing_square_above_crossing_and_upper_stacked(
            groups_by_square=groups_by_square_by_player[1],
        ))
        baseinverse_applied = 0
        if self.threat_combination_type != ThreatCombinationType.OddAboveDirectlyPlayableEven:
            baseinverse_groups, baseinverse_applied = self._threat_combination_baseinverse(
                groups_by_square=groups_by_square_by_player[1],
            )
            problems_solved.update(baseinverse_groups)
        problems_solved.update(self._vertical_groups_in_stacked_column(
            groups_by_square=groups_by_square_by_player[1],
            baseinverse_applied=baseinverse_applied,
        ))
        return problems_solved

    def _no_odd_squares_in_crossing_column(self, groups_by_square: List[List[Set[Group]]]) -> Set[Group]:
        problems_solved = set()

        # Add Groups containing any odd Square in the crossing column that are not directly playable.
        for row in range(self.shared_square.row, self.directly_playable_square_shared_col.row, 2):
            problems_solved.update(groups_by_square[row][self.shared_square.col])

        return problems_solved

    def _no_squares_above_crossing_and_above_odd(self, groups_by_square: List[List[Set[Group]]]) -> Set[Group]:
        problems_solved = set()

        # Add Groups containing a Square above the crossing square and
        # a Square above the odd Square in the stacked column.
        for row_in_crossing_col in range(0, self.shared_square.row, 1):
            for row_in_stacked_col in range(0, self.odd_square.row, 1):
                square_above_crossing_groups = groups_by_square[row_in_crossing_col][self.shared_square.col]
                square_above_stacked_groups = groups_by_square[row_in_stacked_col][self.odd_square.col]
                problems_solved.update(square_above_crossing_groups.intersection(square_above_stacked_groups))

        return problems_solved

    def _groups_containing_square_above_crossing_and_upper_stacked(
            self, groups_by_square: List[List[Set[Group]]]) -> Set[Group]:
        # Add Groups containing the Square above the crossing square and the upper Square in the stacked column.
        square_above_crossing_groups = groups_by_square[self.shared_square.row - 1][self.shared_square.col]
        upper_stacked_square = self.upper_square_in_stacked_column()
        upper_square_in_stacked_column_groups = groups_by_square[upper_stacked_square.row][upper_stacked_square.col]

        return square_above_crossing_groups.intersection(upper_square_in_stacked_column_groups)

    def _highest_crossing_square_if_odd_is_playable(
            self, groups_by_square: List[List[Set[Group]]]) -> Set[Group]:
        problems_solved = set()

        # If the odd square in the stacked column is playable:
        if self.odd_square == self.directly_playable_square_stacked_col:
            # Add Groups containing any Square above square_above_crossing.
            for row in range(self.shared_square.row - 1):
                problems_solved.update(groups_by_square[row][self.shared_square.col])

        return problems_solved

    def _threat_combination_baseinverse(self, groups_by_square: List[List[Set[Group]]]) -> (Set[Group], int):
        # If the first empty square in the crossing column is odd and
        # the odd square in the stacked column is not directly playable:
        if (self.directly_playable_square_shared_col.row % 2 == 1 and
                self.odd_square != self.directly_playable_square_stacked_col):
            # Add Groups containing the lowest squares of both columns.
            baseinverse = Baseinverse(
                playable1=self.directly_playable_square_shared_col,
                playable2=self.directly_playable_square_stacked_col,
            )
            problems_solved = baseinverse.find_problems_solved_for_player(groups_by_square=groups_by_square)

            return problems_solved, 1 if problems_solved else 0

        return {}, 0

    def _vertical_groups_in_stacked_column(
            self, groups_by_square: List[List[Set[Group]]], baseinverse_applied: int) -> Set[Group]:
        problems_solved = set()

        # In the stacked column, add Groups containing two Squares on top of each other
        # up to and including the odd square in that column.
        # If a baseinverse is applied for the ThreatCombination, this observation starts one square higher.
        for lower_row in range(self.odd_square.row - 1,
                               self.directly_playable_square_stacked_col.row - baseinverse_applied + 1):
            vertical = Vertical(
                upper=Square(row=lower_row - 1, col=self.odd_square.col),
                lower=Square(row=lower_row, col=self.odd_square.col),
            )
            problems_solved.update(vertical.find_problems_solved_for_player(groups_by_square=groups_by_square))

        for claimeven_upper_row in range(self.odd_square.row):
            claimeven = Claimeven(
                upper=Square(row=claimeven_upper_row, col=self.odd_square.col),
                lower=Square(row=claimeven_upper_row + 1, col=self.odd_square.col),
            )
            problems_solved.update(claimeven.find_problems_solved_for_player(groups_by_square=groups_by_square))

        return problems_solved


def find_all_threat_combinations(board: Board) -> Set[ThreatCombination]:
    """find_threat_combination returns a ThreatCombination for White if one exists. Otherwise, returns None.
    If multiple threatCombinations exist, picks one arbitrarily.

    Args:
        board (Board): a Board instance.

    Returns:
        threat_combination (ThreatCombination): a ThreatCombination for White if one exists. Otherwise, None.
    """
    white_groups = board.potential_groups(0)

    even_groups = []
    odd_groups = []
    for group in white_groups:
        empty_squares = []
        for square in group.squares:
            if board.is_empty(square):
                empty_squares.append(square)

        if len(empty_squares) != 2:
            continue

        square1, square2 = empty_squares[0], empty_squares[1]
        if square1.row % 2 == 1 and square2.row % 2 == 1:  # odd threat_hunter.
            odd_groups.append(OddGroup(group=group, odd_square1=square1, odd_square2=square2))
        elif square1.row % 2 == 0 and square2.row % 2 == 1:  # even threat_hunter with square1 as the even square.
            even_groups.append(EvenGroup(group=group, odd_square=square2, even_square=square1))
        elif square1.row % 2 == 1 and square2.row % 2 == 0:  # even threat_hunter with square2 as the even square.
            even_groups.append(EvenGroup(group=group, odd_square=square1, even_square=square2))

    threat_combinations = set()
    directly_playable_squares = board.playable_squares()
    for even_threat in even_groups:
        for odd_threat in odd_groups:
            threat_combination = create_threat_combination(
                even_group=even_threat,
                odd_group=odd_threat,
                directly_playable_squares=directly_playable_squares,
            )
            if threat_combination is not None:
                threat_combinations.add(threat_combination)

    return threat_combinations


def create_threat_combination(
        even_group: EvenGroup,
        odd_group: OddGroup,
        directly_playable_squares: Set[Square]) -> Optional[ThreatCombination]:
    odd_unshared_square = get_odd_unshared_square(even_group=even_group, odd_group=odd_group)
    if odd_unshared_square is None:
        return None
    if even_group.even_square.col != odd_unshared_square.col:
        return None

    if even_group.even_square.row - odd_unshared_square.row == -1:
        threat_combination_type = ThreatCombinationType.EvenAboveOdd
    elif even_group.even_square.row - odd_unshared_square.row == 1:
        if even_group.even_square in directly_playable_squares:
            threat_combination_type = ThreatCombinationType.OddAboveDirectlyPlayableEven
        else:
            threat_combination_type = ThreatCombinationType.OddAboveNotDirectlyPlayableEven
    else:
        return None

    directly_playable_square_shared_col = None
    directly_playable_square_stacked_col = None
    for square in directly_playable_squares:
        if square.col == even_group.odd_square.col:
            directly_playable_square_shared_col = square
        if square.col == odd_unshared_square.col:
            directly_playable_square_stacked_col = square

    return ThreatCombination(
        even_group=even_group.group,
        odd_group=odd_group.group,
        shared_square=even_group.odd_square,
        even_square=even_group.even_square,
        odd_square=odd_unshared_square,
        directly_playable_square_shared_col=directly_playable_square_shared_col,
        directly_playable_square_stacked_col=directly_playable_square_stacked_col,
        threat_combination_type=threat_combination_type,
    )


def get_odd_unshared_square(even_group: EvenGroup, odd_group: OddGroup) -> Square:
    if even_group.odd_square == odd_group.odd_square1:
        return odd_group.odd_square2
    if even_group.odd_square == odd_group.odd_square2:
        return odd_group.odd_square1
