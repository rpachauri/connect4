from typing import Dict, Set, FrozenSet

from connect_four.evaluation.victor.rules.threat_combination import ThreatCombinationType
from connect_four.game import Square
from connect_four.evaluation.board import Board

from connect_four.evaluation.victor.rules import Claimeven, find_all_threat_combinations
from connect_four.evaluation.victor.rules import Baseinverse
from connect_four.evaluation.victor.rules import Vertical
from connect_four.evaluation.victor.rules import Aftereven
from connect_four.evaluation.victor.rules import Lowinverse
from connect_four.evaluation.victor.rules import Highinverse
from connect_four.evaluation.victor.rules import Baseclaim
from connect_four.evaluation.victor.rules import Before
from connect_four.evaluation.victor.rules import Specialbefore
from connect_four.evaluation.victor.rules import Oddthreat
from connect_four.evaluation.victor.rules import ThreatCombination

from connect_four.evaluation.victor.rules import find_all_claimevens
from connect_four.evaluation.victor.rules import find_all_baseinverses
from connect_four.evaluation.victor.rules import find_all_verticals
from connect_four.evaluation.victor.rules import find_all_afterevens
from connect_four.evaluation.victor.rules import find_all_lowinverses
from connect_four.evaluation.victor.rules import find_all_highinverses_using_highinverse_columns
from connect_four.evaluation.victor.rules import find_all_baseclaims
from connect_four.evaluation.victor.rules import find_all_befores
from connect_four.evaluation.victor.rules import find_all_specialbefores
from connect_four.evaluation.victor.rules import find_all_oddthreats
from connect_four.problem import Group


class Solution:
    """A Solution is an application of a Rule that refutes at least one group.

    Two Solutions may or may not work together depending on which squares each
    consists of and which rule they are an application of.
    """
    def __init__(self, rule_instance, squares, groups=None, claimeven_bottom_squares=None):
        self.squares = frozenset(squares)

        if groups is None:
            groups = set()
        self.groups = frozenset(groups)

        if claimeven_bottom_squares is None:
            claimeven_bottom_squares = set()
        self.claimeven_bottom_squares = frozenset(claimeven_bottom_squares)

        self.rule_instance = rule_instance
        self.squares_by_column = self.cols_to_squares(squares=self.squares)

    @staticmethod
    def cols_to_squares(squares: FrozenSet[Square]) -> Dict[int, Set[Square]]:
        """Converts an iterable of Squares into a dictionary of Squares keyed by the column they belong in.

        Args:
            squares (iterable<Square>): an iterable of Square objects.

        Returns:
            col_to_squares_dict (Map<int, Set<Square>>): a dictionary of columns to Squares in that column.
        """
        col_to_squares_dict = {}
        for square in squares:
            if square.col not in col_to_squares_dict:
                col_to_squares_dict[square.col] = set()
            col_to_squares_dict[square.col].add(square)
        return col_to_squares_dict

    def __eq__(self, other):
        if isinstance(other, Solution):
            return (self.squares == other.squares and
                    self.groups == other.groups and
                    self.claimeven_bottom_squares == other.claimeven_bottom_squares)
        return False

    def __hash__(self):
        return (self.squares.__hash__() * 59 +
                self.groups.__hash__() * 37 +
                self.claimeven_bottom_squares.__hash__())


def add_solution_to_group_to_solutions(solution: Solution, group_to_solutions: Dict[Group, Set[Solution]]):
    for group in solution.groups:
        if group not in group_to_solutions:
            group_to_solutions[group] = set()
        group_to_solutions[group].add(solution)


def find_all_solutions(board: Board) -> (Set[Solution], Dict[Group, Set[Solution]]):
    """find_all_solutions finds all Solutions the opponent of the
    current player can employ for the given Board.

    Args:
        board (Board): a Board instance.

    Returns:
        solutions (Set[Solution]): a set of Solutions the opponent of the
            current player can employ for board.
    """
    # opponent_groups are the potential groups that the opponent of the current player has for board.
    opponent_groups = board.potential_groups(1 - board.player)

    # Find all applications of all rules.
    claimevens = find_all_claimevens(board=board)
    baseinverses = find_all_baseinverses(board=board)
    verticals = find_all_verticals(board=board)
    afterevens = find_all_afterevens(board=board, opponent_groups=opponent_groups)
    lowinverses = find_all_lowinverses(verticals=verticals)
    highinverses = find_all_highinverses_using_highinverse_columns(board=board)
    baseclaims = find_all_baseclaims(board=board)
    befores = find_all_befores(board=board, opponent_groups=opponent_groups)
    specialbefores = find_all_specialbefores(board=board, befores=befores)

    # square_to_player_groups is a dict of all Squares on board that map to
    # all groups the current player has that contain that Square.
    square_to_player_groups = board.potential_groups_by_square()

    # Convert each application of each rule into a Solution.
    solutions = set()
    group_to_solutions = {}

    for claimeven in claimevens:
        solution = from_claimeven(claimeven=claimeven, square_to_groups=square_to_player_groups)
        if solution is not None:
            solutions.add(solution)
            add_solution_to_group_to_solutions(solution=solution, group_to_solutions=group_to_solutions)

    for baseinverse in baseinverses:
        solution = from_baseinverse(baseinverse=baseinverse, square_to_groups=square_to_player_groups)
        if solution is not None:
            solutions.add(solution)
            add_solution_to_group_to_solutions(solution=solution, group_to_solutions=group_to_solutions)

    for vertical in verticals:
        solution = from_vertical(vertical=vertical, square_to_groups=square_to_player_groups)
        if solution is not None:
            solutions.add(solution)
            add_solution_to_group_to_solutions(solution=solution, group_to_solutions=group_to_solutions)

    for aftereven in afterevens:
        solution = from_aftereven(aftereven=aftereven, square_to_groups=square_to_player_groups)
        if solution is not None:
            solutions.add(solution)
            add_solution_to_group_to_solutions(solution=solution, group_to_solutions=group_to_solutions)

    for lowinverse in lowinverses:
        solution = from_lowinverse(lowinverse=lowinverse, square_to_groups=square_to_player_groups)
        if solution is not None:
            solutions.add(solution)
            add_solution_to_group_to_solutions(solution=solution, group_to_solutions=group_to_solutions)

    for highinverse in highinverses:
        solution = from_highinverse(highinverse=highinverse, square_to_groups=square_to_player_groups)
        if solution is not None:
            solutions.add(solution)
            add_solution_to_group_to_solutions(solution=solution, group_to_solutions=group_to_solutions)

    for baseclaim in baseclaims:
        solution = from_baseclaim(baseclaim=baseclaim, square_to_groups=square_to_player_groups)
        if solution is not None:
            solutions.add(solution)
            add_solution_to_group_to_solutions(solution=solution, group_to_solutions=group_to_solutions)

    for before in befores:
        solution = from_before(before=before, square_to_groups=square_to_player_groups)
        if solution is not None:
            solutions.add(solution)
            add_solution_to_group_to_solutions(solution=solution, group_to_solutions=group_to_solutions)

    for specialbefore in specialbefores:
        solution = from_specialbefore(specialbefore=specialbefore, square_to_groups=square_to_player_groups)
        if solution is not None:
            solutions.add(solution)
            add_solution_to_group_to_solutions(solution=solution, group_to_solutions=group_to_solutions)

    return solutions, group_to_solutions


def from_claimeven(claimeven: Claimeven, square_to_groups) -> Solution:
    """Converts a Claimeven into a Solution.
    Must solve at least one potential group in order to be converted into a Solution.

    Args:
        claimeven (Claimeven): a Claimeven.
        square_to_groups (Map<Square, Set<Group>>): A dictionary mapping each
            Square to all groups that contain that Square.

    Returns:
        solution (Solution): a Solution if claimeven can be converted into one. None if it can't.
    """
    groups = square_to_groups[claimeven.upper]
    if groups:  # len(groups) > 0
        return Solution(
            squares=[claimeven.upper, claimeven.lower],
            groups=groups,
            claimeven_bottom_squares=[claimeven.lower],
            rule_instance=claimeven,
        )


def from_baseinverse(baseinverse: Baseinverse, square_to_groups) -> Solution:
    """Converts a Baseinverse into a Solution.
    Must solve at least one potential group in order to be converted into a Solution.

    Args:
        baseinverse (Baseinverse): a Baseinverse.
        square_to_groups (Map<Square, Set<Group>>): A dictionary mapping each
            Square to all groups that contain that Square.

    Returns:
        solution (Solution): a Solution if baseinverse can be converted into one. None if it can't.
    """
    square1, square2 = tuple(baseinverse.squares)
    groups1, groups2 = square_to_groups[square1], square_to_groups[square2]
    groups_intersection = groups1.intersection(groups2)
    if groups_intersection:
        squares = frozenset([square1, square2])
        return Solution(squares=squares, groups=groups_intersection, rule_instance=baseinverse)


def from_vertical(vertical: Vertical, square_to_groups) -> Solution:
    """Converts a Vertical into a Solution.
    Must solve at least one potential group in order to be converted into a Solution.

    Args:
        vertical (Vertical): a Vertical.
        square_to_groups (Map<Square, Set<Group>>): A dictionary mapping each
            Square to all groups that contain that Square.

    Returns:
        solution (Solution): a Solution if vertical can be converted into one. None if it can't.
    """
    upper_groups, lower_groups = square_to_groups[vertical.upper], square_to_groups[vertical.lower]
    groups_intersection = upper_groups.intersection(lower_groups)
    if groups_intersection:
        squares = frozenset([vertical.upper, vertical.lower])
        return Solution(squares=squares, groups=groups_intersection, rule_instance=vertical)


def from_aftereven(aftereven: Aftereven, square_to_groups) -> Solution:
    """Converts an Aftereven into a Solution.
    Must solve at least one *new* potential group in order to be converted into a Solution.
    By "new potential group," we mean any group that isn't already solved by one of the Claimevens
    which are part of the Aftereven.

    Args:
        aftereven (Aftereven): an Aftereven.
        square_to_groups (Map<Square, Set<Group>>): A dictionary mapping each
            Square to all groups that contain that Square.

    Returns:
        solution (Solution): a Solution if aftereven can be converted into one. None if it can't.
    """
    groups = set()
    add_new_groups_from_aftereven(
        groups=groups,
        empty_squares_of_aftereven=aftereven.empty_squares_of_aftereven_group(),
        threatening_squares=[],
        square_to_groups=square_to_groups,
    )

    # Aftereven should only be converted into a Solution if it refutes new groups.
    if groups:
        squares_involved = list(aftereven.group.squares)
        claimeven_bottom_squares = []
        for claimeven in aftereven.claimevens:
            claimeven_solution = from_claimeven(claimeven, square_to_groups)
            if claimeven_solution is not None:
                groups.update(claimeven_solution.groups)
            squares_involved.append(claimeven.lower)
            claimeven_bottom_squares.append(claimeven.lower)

        return Solution(
            squares=frozenset(squares_involved),
            groups=frozenset(groups),
            claimeven_bottom_squares=claimeven_bottom_squares,
            rule_instance=aftereven,
        )


def add_new_groups_from_aftereven(groups, empty_squares_of_aftereven, threatening_squares, square_to_groups):
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
        groups (set<Group>): a Set of groups this function will add to.
        empty_squares_of_aftereven (list<Square>):
            A subset of empty Squares that belong to an Aftereven.
            If two Squares from the Aftereven belong in the same column,
                the Square from the higher row should be given.
            It is required that none of the Squares share the same column.
        threatening_squares (list<Square>):
            A list of Squares that could belong to a group that the Aftereven refutes.
            It is required that none of the Squares share the same column.
        square_to_groups (Map<Square, Set<Group>>): A dictionary mapping each
            Square to all groups that contain that Square.

    Returns:
        None
    """
    # Base case.
    if not empty_squares_of_aftereven:
        new_groups_to_add = square_to_groups[threatening_squares[0]]
        for square in threatening_squares[1:]:
            new_groups_to_add = new_groups_to_add.intersection(square_to_groups[square])
        groups.update(new_groups_to_add)
        return

    # Recursive Case.
    square = empty_squares_of_aftereven.pop()
    for row in range(square.row - 1, -1, -1):
        square_above = Square(row=row, col=square.col)
        # Choose.
        threatening_squares.append(square_above)
        # Recurse.
        add_new_groups_from_aftereven(groups, empty_squares_of_aftereven, threatening_squares, square_to_groups)
        # Unchoose.
        threatening_squares.remove(square_above)
    empty_squares_of_aftereven.append(square)


def from_lowinverse(lowinverse: Lowinverse, square_to_groups) -> Solution:
    """Converts a Lowinverse into a Solution.
    Must solve at least one *new* potential group in order to be converted into a Solution.
    By "new potential group," we mean any group that isn't already solved by one of the Verticals
    which are part of the Lowinverse.

    Args:
        lowinverse (Lowinverse): a Lowinverse.
        square_to_groups (Map<Square, Set<Group>>): A dictionary mapping each
            Square to all groups that contain that Square.

    Returns:
        solution (Solution): a Solution if lowinverse can be converted into one. None if it can't.
    """
    verticals_as_list = list(lowinverse.verticals)
    vertical_0, vertical_1 = verticals_as_list[0], verticals_as_list[1]
    groups = square_to_groups[vertical_0.upper].intersection(square_to_groups[vertical_1.upper])

    # Lowinverse should only be converted into a Solution if it refutes new groups.
    if groups:
        squares = [vertical_0.upper, vertical_0.lower, vertical_1.upper, vertical_1.lower]

        vertical_0_solution = from_vertical(vertical_0, square_to_groups)
        vertical_1_solution = from_vertical(vertical_1, square_to_groups)
        if vertical_0_solution is not None:
            groups.update(vertical_0_solution.groups)
        if vertical_1_solution is not None:
            groups.update(vertical_1_solution.groups)

        return Solution(
            squares=frozenset(squares),
            groups=frozenset(groups),
            rule_instance=lowinverse,
        )


def from_highinverse(highinverse: Highinverse, square_to_groups) -> Solution:
    """Converts a Highinverse into a Solution.
    Must solve at least one *new* potential group in order to be converted into a Solution.
    By "new potential group," we mean any group that isn't already solved by the Verticals or Lowinverse
    which are part of the Highinverse.

    Args:
        highinverse (Highinverse): a Highinverse.
        square_to_groups (Map<Square, Set<Group>>): A dictionary mapping each
            Square to all groups that contain that Square.

    Returns:
        solution (Solution): a Solution if highinverse can be converted into one. None if it can't.
    """
    column_0, column_1 = tuple(highinverse.columns)
    squares = frozenset([
        column_0.upper,
        column_0.middle,
        column_0.lower,
        column_1.upper,
        column_1.middle,
        column_1.lower,
    ])

    highinverse_groups = set()
    column_0, column_1 = tuple(highinverse.columns)

    #  Add all groups which contain the two upper squares.
    upper_square_0 = column_0.upper
    upper_square_1 = column_1.upper
    upper_squares_groups = square_to_groups[upper_square_0].intersection(square_to_groups[upper_square_1])
    highinverse_groups.update(upper_squares_groups)

    # Add all groups which contain the two middle squares.
    middle_squares_groups = square_to_groups[column_0.middle].intersection(square_to_groups[column_1.middle])
    highinverse_groups.update(middle_squares_groups)

    # For each Highinverse column, add all (vertical) groups which contain the two highest squares of the
    # column.
    highinverse_groups.update(square_to_groups[column_0.upper].intersection(square_to_groups[column_0.middle]))
    highinverse_groups.update(square_to_groups[column_1.upper].intersection(square_to_groups[column_1.middle]))

    # If the lower square of the first column is directly playable:
    if column_0.directly_playable:
        # Add all groups which contain both the lower square of the first column and
        # the upper square of the second column.
        lower_0_upper_1_groups = square_to_groups[column_0.lower].intersection(square_to_groups[upper_square_1])
        highinverse_groups.update(lower_0_upper_1_groups)

    # If the lower square of the second column is directly playable:
    if column_1.directly_playable:
        # Add all groups which contain both the lower square of the second column and
        # the upper square of the first column.
        lower_1_upper_0_groups = square_to_groups[column_1.lower].intersection(square_to_groups[upper_square_0])
        highinverse_groups.update(lower_1_upper_0_groups)

    return Solution(
        squares=squares,
        groups=frozenset(highinverse_groups),
        rule_instance=highinverse,
    )


def from_baseclaim(baseclaim: Baseclaim, square_to_groups) -> Solution:
    """Converts a Baseclaim into a Solution.
    Must solve at least one potential group in order to be converted into a Solution.

    Args:
        baseclaim (Baseclaim): a Baseclaim.
        square_to_groups (Map<Square, Set<Group>>): A dictionary mapping each
            Square to all groups that contain that Square.

    Returns:
        solution (Solution): a Solution if baseclaim can be converted into one. None if it can't.
    """
    groups = set()

    # Add all groups which contain the first playable square and the square above the second playable
    # square.
    square_above_second = Square(row=baseclaim.second.row - 1, col=baseclaim.second.col)
    groups.update(square_to_groups[baseclaim.first].intersection(square_to_groups[square_above_second]))

    # Add all groups which contain the second and third playable square.
    groups.update(square_to_groups[baseclaim.second].intersection(square_to_groups[baseclaim.third]))

    # If there is at least one group:
    if groups:
        squares = frozenset([baseclaim.first, baseclaim.second, baseclaim.third, square_above_second])
        return Solution(
            squares=squares,
            groups=frozenset(groups),
            claimeven_bottom_squares=[baseclaim.second],
            rule_instance=baseclaim,
        )


def from_before(before: Before, square_to_groups) -> Solution:
    """Converts a Before into a Solution.
    Must solve at least one *new* potential group in order to be converted into a Solution.
    By "new potential group," we mean any group that contains all successors of the empty
    squares in the Before group.

    Args:
        before (Before): a Before.
        square_to_groups (Map<Square, Set<Group>>): A dictionary mapping each
            Square to all groups that contain that Square.

    Returns:
        solution (Solution): a Solution if before can be converted into one. None if it can't.
    """
    empty_squares = before.empty_squares_of_before_group()
    empty_square_successors = []
    for square in empty_squares:
        empty_square_successors.append(Square(row=square.row - 1, col=square.col))

    groups = square_to_groups[empty_square_successors[0]]
    for square in empty_square_successors[1:]:
        groups = groups.intersection(square_to_groups[square])

    # If there is at least one group that contains all direct successors of all empty squares in the Before group:
    if groups:
        squares = set(empty_squares)

        for vertical in before.verticals:
            # Add all squares part of Verticals which are part of the Before.
            squares.add(vertical.upper)
            squares.add(vertical.lower)
            # Add all groups refuted by Verticals which are part of the Before.
            vertical_solution = from_vertical(vertical, square_to_groups)
            if vertical_solution:
                groups.update(vertical_solution.groups)

        claimeven_bottom_squares = []
        for claimeven in before.claimevens:
            # Add all squares part of Claimevens which are part of the Before.
            squares.add(claimeven.upper)
            squares.add(claimeven.lower)
            claimeven_bottom_squares.append(claimeven.lower)
            # Add all groups refuted by Claimevens which are part of the Before.
            claimeven_solution = from_claimeven(claimeven, square_to_groups)
            if claimeven_solution:
                groups.update(claimeven_solution.groups)

        return Solution(
            squares=frozenset(squares),
            groups=frozenset(groups),
            claimeven_bottom_squares=claimeven_bottom_squares,
            rule_instance=before,
        )


def from_specialbefore(specialbefore: Specialbefore, square_to_groups) -> Solution:
    """Converts a Specialbefore into a Solution.
    Must solve at least one *new* potential group in order to be converted into a Solution.
    By "new potential group," we mean groups that meet either of the following conditions:
    1. groups that contain the external directly playable square and
       all successors of empty squares of the Specialbefore.
    2. groups that contain the internal directly playable square and external directly playable square
       of the Specialbefore.

    Args:
        specialbefore (Specialbefore): a Specialbefore.
        square_to_groups (Map<Square, Set<Group>>): A dictionary mapping each
            Square to all groups that contain that Square.

    Returns:
        solution (Solution): a Solution if before can be converted into one. None if it can't.
    """
    # Find all groups that contain the external directly playable square and
    # all successors of empty squares of the Specialbefore.
    external_and_successor_groups = square_to_groups[specialbefore.external_directly_playable_square]
    empty_squares = specialbefore.before.empty_squares_of_before_group()
    for square in empty_squares:
        direct_successor = Square(row=square.row - 1, col=square.col)
        external_and_successor_groups = external_and_successor_groups.intersection(
            square_to_groups[direct_successor])

    if external_and_successor_groups:
        # Find all groups that contain the internal directly playable square and
        # external directly playable square of the Specialbefore.
        # Essentially, reproducing the groups refuted by a Baseinverse.
        sq1 = specialbefore.internal_directly_playable_square
        sq2 = specialbefore.external_directly_playable_square
        directly_playable_squares_groups = square_to_groups[sq1].intersection(square_to_groups[sq2])

        squares = {sq1, sq2}
        groups = external_and_successor_groups.union(directly_playable_squares_groups)

        for vertical in specialbefore.before.verticals:
            if vertical != specialbefore.unused_vertical:
                # Add all squares part of Verticals which are part of the Before.
                squares.add(vertical.upper)
                squares.add(vertical.lower)
                # Add all groups refuted by Verticals which are part of the Before.
                vertical_solution = from_vertical(vertical, square_to_groups)
                if vertical_solution:
                    groups.update(vertical_solution.groups)

        claimeven_bottom_squares = []
        for claimeven in specialbefore.before.claimevens:
            # Add all squares part of Claimevens which are part of the Before.
            squares.add(claimeven.upper)
            squares.add(claimeven.lower)
            claimeven_bottom_squares.append(claimeven.lower)
            # Add all groups refuted by Claimevens which are part of the Before.
            claimeven_solution = from_claimeven(claimeven, square_to_groups)
            if claimeven_solution:
                groups.update(claimeven_solution.groups)

        # The Specialbefore Solution includes all squares and groups that the Before Solution has.
        return Solution(
            squares=frozenset(squares),
            groups=frozenset(groups),
            claimeven_bottom_squares=claimeven_bottom_squares,
            rule_instance=specialbefore,
        )


def find_all_win_conditions(board: Board) -> Set[Solution]:
    """find_all_win_conditions finds all Solutions the opponent of the
        current player can employ for the given Board.

        Args:
            board (Board): a Board instance.

        Returns:
            solutions (Set[Solution]): a set of Solutions the opponent of the
                current player can employ for board. All are win conditions.
        """
    oddthreats = find_all_oddthreats(board=board)
    threat_combinations = find_all_threat_combinations(board=board)

    # square_to_player_groups is a dict of all Squares on board that map to
    # all groups the current player has that contain that Square.
    square_to_player_groups = board.potential_groups_by_square()

    # Convert each win condition into a Solution.
    solutions = set()
    for oddthreat in oddthreats:
        solution = from_oddthreat(oddthreat=oddthreat, square_to_groups=square_to_player_groups)
        solutions.add(solution)

    for threat_combination in threat_combinations:
        if threat_combination.threat_combination_type == ThreatCombinationType.EvenAboveOdd:
            solution = from_even_above_odd_threat_combination(
                threat_combination=threat_combination, square_to_groups=square_to_player_groups)
            solutions.add(solution)
        elif threat_combination.threat_combination_type == ThreatCombinationType.OddAboveNotDirectlyPlayableEven:
            solution = from_odd_above_even_not_directly_playable_threat_combination(
                threat_combination=threat_combination, square_to_groups=square_to_player_groups)
            solutions.add(solution)
        else:  # threat_combination.threat_combination_type == ThreatCombinationType.OddAboveDirectlyPlayableEven:
            solution = from_odd_above_even_directly_playable_threat_combination(
                threat_combination=threat_combination, square_to_groups=square_to_player_groups)
            solutions.add(solution)

    return solutions


def from_oddthreat(oddthreat: Oddthreat, square_to_groups: Dict[Square, Set[Group]]) -> Solution:
    groups_solved = set()

    # Add Groups containing any odd Square up to the Odd Threat that are not directly playable.
    for row in range(oddthreat.empty_square.row, oddthreat.directly_playable_square.row, 2):
        square = Square(row=row, col=oddthreat.empty_square.col)
        groups_solved.update(square_to_groups[square])

    # Add Groups containing any Squares above the odd Threat.
    for row in range(0, oddthreat.empty_square.row, 1):
        square = Square(row=row, col=oddthreat.empty_square.col)
        groups_solved.update(square_to_groups[square])

    return Solution(
        rule_instance=oddthreat,
        squares=[oddthreat.empty_square],
        groups=groups_solved,
    )


def from_even_above_odd_threat_combination(
        threat_combination: ThreatCombination, square_to_groups: Dict[Square, Set[Group]]) -> Solution:
    groups_solved = set()

    # 1. Black gets no odd squares in the crossing column (except for a first directly playable square).
    groups_solved.update(no_odd_squares_in_crossing_column(
        threat_combination=threat_combination, square_to_groups=square_to_groups,
    ))
    # 2. Black will not get both a square above the crossing square and a square above the odd square in the
    # other column.
    groups_solved.update(no_squares_above_crossing_and_above_odd(
        threat_combination=threat_combination, square_to_groups=square_to_groups,
    ))
    # 3. Black will not get both the square above the crossing square and the odd square in the other column.
    groups_solved.update(groups_containing_square_above_crossing_and_odd(
        threat_combination=threat_combination, square_to_groups=square_to_groups,
    ))
    # 4. If the odd square in the other column is playable, the highest square in the crossing column which
    # can be taken by Black, is the square directly above the crossing square.
    groups_solved.update(highest_crossing_square_if_odd_is_playable(
        threat_combination=threat_combination, square_to_groups=square_to_groups,
    ))
    # 5. If the first empty square in the crossing column is odd and the odd square in the other column is
    # not directly playable, a Baseinverse can be used on the lowest squares of both columns.
    baseinverse_groups, baseinverse_applied = threat_combination_baseinverse(
        threat_combination=threat_combination, square_to_groups=square_to_groups,
    )
    groups_solved.update(baseinverse_groups)
    # 6. In the other column each move of the opponent will be answered, giving (at least) one out of every
    # two points to the solving player up to and including the odd square in that column. If rule 5 is
    # applied, this observation starts one square higher.
    groups_solved.update(vertical_groups_in_stacked_column(
        threat_combination=threat_combination,
        square_to_groups=square_to_groups,
        baseinverse_applied=baseinverse_applied,
    ))

    return Solution(
        rule_instance=threat_combination,
        squares=[threat_combination.shared_square, threat_combination.odd_square],
        groups=groups_solved,
    )


def from_odd_above_even_not_directly_playable_threat_combination(
        threat_combination: ThreatCombination, square_to_groups: Dict[Square, Set[Group]]) -> Solution:
    groups_solved = set()

    # 1. Black gets no odd squares in the crossing column (except for a first directly playable square).
    groups_solved.update(no_odd_squares_in_crossing_column(
        threat_combination=threat_combination, square_to_groups=square_to_groups,
    ))
    # 2. Black will not get both a square above the crossing square and a square above the odd square in the
    # other column.
    groups_solved.update(no_squares_above_crossing_and_above_odd(
        threat_combination=threat_combination, square_to_groups=square_to_groups,
    ))
    # 3. If the first empty square in the crossing column is odd and the odd square in the other column is
    # not directly playable, a Baseinverse can be used on the lowest squares of both columns.
    baseinverse_groups, baseinverse_applied = threat_combination_baseinverse(
        threat_combination=threat_combination, square_to_groups=square_to_groups,
    )
    groups_solved.update(baseinverse_groups)
    # 4. In the other column each move of the opponent will be answered, giving (at least) one out of every
    # two points to the solving player up to and including the odd square in that column. If rule 3 is
    # applied, this observation starts one square higher.
    groups_solved.update(vertical_groups_in_stacked_column(
        threat_combination=threat_combination,
        square_to_groups=square_to_groups,
        baseinverse_applied=baseinverse_applied,
    ))

    return Solution(
        rule_instance=threat_combination,
        squares=[threat_combination.shared_square, threat_combination.odd_square],
        groups=groups_solved,
    )


def from_odd_above_even_directly_playable_threat_combination(
        threat_combination: ThreatCombination, square_to_groups: Dict[Square, Set[Group]]) -> Solution:
    groups_solved = set()

    # 1. Black gets no odd squares in the crossing column (except for a first directly playable square).
    groups_solved.update(no_odd_squares_in_crossing_column(
        threat_combination=threat_combination, square_to_groups=square_to_groups,
    ))
    # 2. Black will not get both a square above the crossing square and a square above the odd square in the
    # other column.
    groups_solved.update(no_squares_above_crossing_and_above_odd(
        threat_combination=threat_combination, square_to_groups=square_to_groups,
    ))

    return Solution(
        rule_instance=threat_combination,
        squares=[threat_combination.shared_square, threat_combination.odd_square],
        groups=groups_solved,
    )


def no_odd_squares_in_crossing_column(
        threat_combination: ThreatCombination, square_to_groups: Dict[Square, Set[Group]]) -> Set[Group]:
    problems_solved = set()

    # Add Groups containing any odd Square in the crossing column that are not directly playable.
    for row in range(1, threat_combination.directly_playable_square_shared_col.row, 2):
        square = Square(row=row, col=threat_combination.shared_square.col)
        problems_solved.update(square_to_groups[square])

    return problems_solved


def no_squares_above_crossing_and_above_odd(
        threat_combination: ThreatCombination, square_to_groups: Dict[Square, Set[Group]]) -> Set[Group]:
    problems_solved = set()

    # Add Groups containing a Square above the crossing square and
    # a Square above the odd Square in the stacked column.
    for row_in_crossing_col in range(0, threat_combination.shared_square.row, 1):
        for row_in_stacked_col in range(0, threat_combination.odd_square.row, 1):
            square_above_crossing = Square(row=row_in_crossing_col, col=threat_combination.shared_square.col)
            square_above_stacked = Square(row=row_in_stacked_col, col=threat_combination.odd_square.col)
            square_above_crossing_groups = square_to_groups[square_above_crossing]
            square_above_stacked_groups = square_to_groups[square_above_stacked]
            problems_solved.update(square_above_crossing_groups.intersection(square_above_stacked_groups))

    return problems_solved


def groups_containing_square_above_crossing_and_odd(
        threat_combination: ThreatCombination, square_to_groups: Dict[Square, Set[Group]]) -> Set[Group]:
    # Add Groups containing the Square above the crossing square and the upper Square in the stacked column.
    square_above_crossing = Square(
        row=threat_combination.shared_square.row - 1,
        col=threat_combination.shared_square.col,
    )
    square_above_crossing_groups = square_to_groups[square_above_crossing]
    odd_square_groups = square_to_groups[threat_combination.odd_square]

    return square_above_crossing_groups.intersection(odd_square_groups)


def highest_crossing_square_if_odd_is_playable(
        threat_combination: ThreatCombination, square_to_groups: Dict[Square, Set[Group]]) -> Set[Group]:
    problems_solved = set()

    # If the odd square in the stacked column is playable:
    if threat_combination.odd_square == threat_combination.directly_playable_square_stacked_col:
        # Add Groups containing any Square above square_above_crossing.
        for row in range(threat_combination.shared_square.row - 1):
            square = Square(row=row, col=threat_combination.shared_square.col)
            problems_solved.update(square_to_groups[square])

    return problems_solved


def threat_combination_baseinverse(
        threat_combination: ThreatCombination, square_to_groups: Dict[Square, Set[Group]]) -> (Set[Group], int):
    # If the first empty square in the crossing column is odd and
    # the odd square in the stacked column is not directly playable:
    if (threat_combination.directly_playable_square_shared_col.row % 2 == 1 and
            threat_combination.odd_square != threat_combination.directly_playable_square_stacked_col):
        # Add Groups containing the lowest squares of both columns.
        problems_solved = square_to_groups[threat_combination.directly_playable_square_shared_col].intersection(
            square_to_groups[threat_combination.directly_playable_square_stacked_col],
        )

        return problems_solved, 1 if problems_solved else 0

    return {}, 0


def vertical_groups_in_stacked_column(
        threat_combination: ThreatCombination,
        square_to_groups: Dict[Square, Set[Group]],
        baseinverse_applied: int) -> Set[Group]:
    problems_solved = set()

    # In the stacked column, add Groups containing two Squares on top of each other
    # up to and including the odd square in that column.
    # If a baseinverse is applied for the ThreatCombination, this observation starts one square higher.
    for lower_row in range(threat_combination.odd_square.row,
                           threat_combination.directly_playable_square_stacked_col.row - baseinverse_applied + 1):
        upper = Square(row=lower_row - 1, col=threat_combination.odd_square.col)
        lower = Square(row=lower_row, col=threat_combination.odd_square.col)
        problems_solved.update(square_to_groups[upper].intersection(square_to_groups[lower]))

    return problems_solved
