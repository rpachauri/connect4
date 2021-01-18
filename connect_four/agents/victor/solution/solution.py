from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Board

from connect_four.agents.victor.rules import Rule
from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Aftereven
from connect_four.agents.victor.rules import Lowinverse
from connect_four.agents.victor.rules import Highinverse
from connect_four.agents.victor.rules import Baseclaim
from connect_four.agents.victor.rules import Before
from connect_four.agents.victor.rules import Specialbefore

from connect_four.agents.victor.rules import find_all_claimevens
from connect_four.agents.victor.rules import find_all_baseinverses
from connect_four.agents.victor.rules import find_all_verticals
from connect_four.agents.victor.rules import find_all_afterevens
from connect_four.agents.victor.rules import find_all_lowinverses
from connect_four.agents.victor.rules import find_all_highinverses
from connect_four.agents.victor.rules import find_all_baseclaims
from connect_four.agents.victor.rules import find_all_befores
from connect_four.agents.victor.rules import find_all_specialbefores

from connect_four.agents.victor.planning import plan


class Solution:
    """A Solution is an application of a Rule that refutes at least one threat.

    Two Solutions may or may not work together depending on which squares each
    consists of and which rule they are an application of.
    """
    def __init__(self, rule, squares, threats=None, claimeven_bottom_squares=None, solution_plan=None):
        self.rule = rule
        self.squares = frozenset(squares)

        if threats is None:
            threats = set()
        self.threats = frozenset(threats)

        if claimeven_bottom_squares is None:
            claimeven_bottom_squares = set()
        self.claimeven_bottom_squares = frozenset(claimeven_bottom_squares)

        self.plan = solution_plan

    def __eq__(self, other):
        if isinstance(other, Solution):
            return (self.rule == other.rule and
                    self.squares == other.squares and
                    self.threats == other.threats and
                    self.claimeven_bottom_squares == other.claimeven_bottom_squares and
                    self.plan == other.plan)
        return False

    def __hash__(self):
        return (self.rule.__hash__() * 73 +
                self.squares.__hash__() * 59 +
                self.threats.__hash__() * 37 +
                self.claimeven_bottom_squares.__hash__() * 31 +
                self.plan.__hash__())


def find_all_solutions(board: Board):
    """find_all_solutions finds all Solutions the opponent of the
    current player can employ for the given Board.

    Args:
        board (Board): a Board instance.

    Returns:
        solutions (Set<Solution>): a set of Solutions the opponent of the
            current player can employ for board.
    """
    # opponent_threats are the potential Threats that the opponent of the current player has for board.
    opponent_threats = board.potential_threats(1 - board.player)

    # Find all applications of all rules.
    claimevens = find_all_claimevens(board=board)
    baseinverses = find_all_baseinverses(board=board)
    verticals = find_all_verticals(board=board)
    afterevens = find_all_afterevens(board=board, claimevens=claimevens)
    lowinverses = find_all_lowinverses(verticals=verticals)
    highinverses = find_all_highinverses(lowinverses=lowinverses)
    baseclaims = find_all_baseclaims(board=board)
    befores = find_all_befores(board=board, threats=opponent_threats)
    specialbefores = find_all_specialbefores(board=board, befores=befores)

    # square_to_player_threats is a dict of all Squares on board that map to
    # all Threats the current player has that contain that Square.
    square_to_player_threats = board.potential_threats_by_square()

    # Convert each application of each rule into a Solution.
    solutions = set()

    for claimeven in claimevens:
        solution = from_claimeven(claimeven=claimeven, square_to_threats=square_to_player_threats)
        if solution is not None:
            solutions.add(solution)

    for baseinverse in baseinverses:
        solution = from_baseinverse(baseinverse=baseinverse, square_to_threats=square_to_player_threats)
        if solution is not None:
            solutions.add(solution)

    for vertical in verticals:
        solution = from_vertical(vertical=vertical, square_to_threats=square_to_player_threats)
        if solution is not None:
            solutions.add(solution)

    for aftereven in afterevens:
        solution = from_aftereven(aftereven=aftereven, square_to_threats=square_to_player_threats)
        if solution is not None:
            solutions.add(solution)

    for lowinverse in lowinverses:
        solution = from_lowinverse(lowinverse=lowinverse, square_to_threats=square_to_player_threats)
        if solution is not None:
            solutions.add(solution)

    for highinverse in highinverses:
        solution = from_highinverse(
            highinverse=highinverse,
            square_to_threats=square_to_player_threats,
            directly_playable_squares=board.playable_squares()
        )
        if solution is not None:
            solutions.add(solution)

    for baseclaim in baseclaims:
        solution = from_baseclaim(baseclaim=baseclaim, square_to_threats=square_to_player_threats)
        if solution is not None:
            solutions.add(solution)

    for before in befores:
        solution = from_before(before=before, square_to_threats=square_to_player_threats)
        if solution is not None:
            solutions.add(solution)

    for specialbefore in specialbefores:
        solution = from_specialbefore(specialbefore=specialbefore, square_to_threats=square_to_player_threats)
        if solution is not None:
            solutions.add(solution)

    return solutions


def from_claimeven(claimeven: Claimeven, square_to_threats) -> Solution:
    """Converts a Claimeven into a Solution.
    Must solve at least one potential threat in order to be converted into a Solution.

    Args:
        claimeven (Claimeven): a Claimeven.
        square_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if claimeven can be converted into one. None if it can't.
    """
    threats = square_to_threats[claimeven.upper]
    if threats:  # len(threats) > 0
        return Solution(
            rule=Rule.Claimeven,
            squares=[claimeven.upper, claimeven.lower],
            threats=threats,
            claimeven_bottom_squares=[claimeven.lower],
            solution_plan=plan.from_claimeven(claimeven=claimeven),
        )


def from_baseinverse(baseinverse: Baseinverse, square_to_threats) -> Solution:
    """Converts a Baseinverse into a Solution.
    Must solve at least one potential threat in order to be converted into a Solution.

    Args:
        baseinverse (Baseinverse): a Baseinverse.
        square_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if baseinverse can be converted into one. None if it can't.
    """
    square1, square2 = tuple(baseinverse.squares)
    threats1, threats2 = square_to_threats[square1], square_to_threats[square2]
    threats_intersection = threats1.intersection(threats2)
    if threats_intersection:
        squares = frozenset([square1, square2])
        return Solution(rule=Rule.Baseinverse, squares=squares, threats=threats_intersection)


def from_vertical(vertical: Vertical, square_to_threats) -> Solution:
    """Converts a Vertical into a Solution.
    Must solve at least one potential threat in order to be converted into a Solution.

    Args:
        vertical (Vertical): a Vertical.
        square_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if vertical can be converted into one. None if it can't.
    """
    upper_threats, lower_threats = square_to_threats[vertical.upper], square_to_threats[vertical.lower]
    threats_intersection = upper_threats.intersection(lower_threats)
    if threats_intersection:
        squares = frozenset([vertical.upper, vertical.lower])
        return Solution(rule=Rule.Vertical, squares=squares, threats=threats_intersection)


def from_aftereven(aftereven: Aftereven, square_to_threats) -> Solution:
    """Converts an Aftereven into a Solution.
    Must solve at least one *new* potential threat in order to be converted into a Solution.
    By "new potential threat," we mean any threat that isn't already solved by one of the Claimevens
    which are part of the Aftereven.

    Args:
        aftereven (Aftereven): an Aftereven.
        square_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if aftereven can be converted into one. None if it can't.
    """
    # columns_to_highest_rows is a dictionary mapping each column in the Aftereven group to the
    # row with the highest empty Square in the Aftereven group.
    columns_to_highest_rows = {}
    for claimeven in aftereven.claimevens:
        square = claimeven.upper
        if square.col not in columns_to_highest_rows:
            columns_to_highest_rows[square.col] = square.row
        else:
            columns_to_highest_rows[square.col] = min(columns_to_highest_rows[square], square.row)

    # empty_squares_of_aftereven contains the empty Squares of the Aftereven group.
    # If multiple Squares belonged to the same column, then only the Square in the highest row is included.
    empty_squares_of_aftereven = []
    for col in columns_to_highest_rows:
        empty_squares_of_aftereven.append(Square(row=columns_to_highest_rows[col], col=col))

    threats = set()
    add_new_threats_from_aftereven(
        threats=threats,
        empty_squares_of_aftereven=empty_squares_of_aftereven,
        threatening_squares=[],
        square_to_threats=square_to_threats,
    )

    # Aftereven should only be converted into a Solution if it refutes new threats.
    if threats:
        squares_involved = list(aftereven.threat.squares)
        claimeven_bottom_squares = []
        for claimeven in aftereven.claimevens:
            claimeven_solution = from_claimeven(claimeven, square_to_threats)
            threats.update(claimeven_solution.threats)
            squares_involved.append(claimeven.lower)
            claimeven_bottom_squares.append(claimeven.lower)

        return Solution(
            rule=Rule.Aftereven,
            squares=frozenset(squares_involved),
            threats=frozenset(threats),
            claimeven_bottom_squares=claimeven_bottom_squares,
        )


def add_new_threats_from_aftereven(threats, empty_squares_of_aftereven, threatening_squares, square_to_threats):
    """Adds any new threats that intersect squares above empty_squares_of_aftereven to threats.
    This is a recursive backtracking algorithm.
    threatening_squares starts out as an empty list.
    empty_squares_of_aftereven starts out as a list of all empty squares of the aftereven.

    We select a square from empty_squares_of_aftereven and remove it from the list.
    For every square above that square, we add it to threatening_squares, recurse, and then remove it from
      threatening_squares.
    The base case is when empty_squares_of_aftereven is empty. At that point, we find all threats that include
      all squares in threatening_squares and add them to threats.

    Args:
        threats (set<Threat>): a Set of Threats this function will add to.
        empty_squares_of_aftereven (list<Square>):
            A subset of empty Squares that belong to an Aftereven.
            If two Squares from the Aftereven belong in the same column,
                the Square from the higher row should be given.
            It is required that none of the Squares share the same column.
        threatening_squares (list<Square>):
            A list of Squares that could belong to a threat that the Aftereven refutes.
            It is required that none of the Squares share the same column.
        square_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        None
    """
    # Base case.
    if not empty_squares_of_aftereven:
        new_threats_to_add = square_to_threats[threatening_squares[0]]
        for square in threatening_squares[1:]:
            new_threats_to_add = new_threats_to_add.intersection(square_to_threats[square])
        threats.update(new_threats_to_add)
        return

    # Recursive Case.
    square = empty_squares_of_aftereven.pop()
    for row in range(square.row - 1, -1, -1):
        square_above = Square(row=row, col=square.col)
        # Choose.
        threatening_squares.append(square_above)
        # Recurse.
        add_new_threats_from_aftereven(threats, empty_squares_of_aftereven, threatening_squares, square_to_threats)
        # Unchoose.
        threatening_squares.remove(square_above)
    empty_squares_of_aftereven.append(square)


def from_lowinverse(lowinverse: Lowinverse, square_to_threats) -> Solution:
    """Converts a Lowinverse into a Solution.
    Must solve at least one *new* potential threat in order to be converted into a Solution.
    By "new potential threat," we mean any threat that isn't already solved by one of the Verticals
    which are part of the Lowinverse.

    Args:
        lowinverse (Lowinverse): a Lowinverse.
        square_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if lowinverse can be converted into one. None if it can't.
    """
    verticals_as_list = list(lowinverse.verticals)
    vertical_0, vertical_1 = verticals_as_list[0], verticals_as_list[1]
    threats = square_to_threats[vertical_0.upper].intersection(square_to_threats[vertical_1.upper])

    # Lowinverse should only be converted into a Solution if it refutes new threats.
    if threats:
        squares = [vertical_0.upper, vertical_0.lower, vertical_1.upper, vertical_1.lower]

        vertical_0_solution = from_vertical(vertical_0, square_to_threats)
        vertical_1_solution = from_vertical(vertical_1, square_to_threats)
        if vertical_0_solution is not None:
            threats.update(vertical_0_solution.threats)
        if vertical_1_solution is not None:
            threats.update(vertical_1_solution.threats)

        return Solution(
            rule=Rule.Lowinverse,
            squares=frozenset(squares),
            threats=frozenset(threats),
        )


def from_highinverse(highinverse: Highinverse, square_to_threats, directly_playable_squares) -> Solution:
    """Converts a Highinverse into a Solution.
    Must solve at least one *new* potential threat in order to be converted into a Solution.
    By "new potential threat," we mean any threat that isn't already solved by the Verticals or Lowinverse
    which are part of the Highinverse.

    Args:
        highinverse (Highinverse): a Highinverse.
        square_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.
        directly_playable_squares (Set<Square>): A Set of directly playable Squares.

    Returns:
        solution (Solution): a Solution if highinverse can be converted into one. None if it can't.
    """
    highinverse_threats = set()

    # Add all threats which contain the two upper squares.
    verticals_as_list = list(highinverse.lowinverse.verticals)
    vertical_0, vertical_1 = verticals_as_list[0], verticals_as_list[1]
    upper_square_0 = Square(row=vertical_0.upper.row - 1, col=vertical_0.upper.col)
    upper_square_1 = Square(row=vertical_1.upper.row - 1, col=vertical_1.upper.col)
    upper_squares_threats = square_to_threats[upper_square_0].intersection(square_to_threats[upper_square_1])
    highinverse_threats.update(upper_squares_threats)

    # Add all threats which contain the two middle squares.
    middle_squares_threats = square_to_threats[vertical_0.upper].intersection(square_to_threats[vertical_1.upper])
    highinverse_threats.update(middle_squares_threats)

    # For each Highinverse column, add all (vertical) threats which contain the two highest squares of the column.
    upper_vertical_0 = Vertical(upper=upper_square_0, lower=vertical_0.upper)
    upper_vertical_1 = Vertical(upper=upper_square_1, lower=vertical_1.upper)
    upper_vertical_0_solution = from_vertical(upper_vertical_0, square_to_threats)
    upper_vertical_1_solution = from_vertical(upper_vertical_1, square_to_threats)
    if upper_vertical_0_solution is not None:
        highinverse_threats.update(upper_vertical_0_solution.threats)
    if upper_vertical_1_solution is not None:
        highinverse_threats.update(upper_vertical_1_solution.threats)

    # If the lower square of the first column is directly playable:
    if vertical_0.lower in directly_playable_squares:
        # Add all threats which contain both the lower square of the first column and
        # the upper square of the second column.
        lower_0_upper_1_threats = square_to_threats[vertical_0.lower].intersection(square_to_threats[upper_square_1])
        highinverse_threats.update(lower_0_upper_1_threats)

    # If the lower square of the second column is directly playable:
    if vertical_1.lower in directly_playable_squares:
        # Add all threats which contain both the lower square of the second column and
        # the upper square of the first column.
        lower_1_upper_0_threats = square_to_threats[vertical_1.lower].intersection(square_to_threats[upper_square_0])
        highinverse_threats.update(lower_1_upper_0_threats)

    # already_solved_threats are all Threats that are already solved by vertical_0, vertical_1 or lowinverse.
    already_solved_threats = set()
    vertical_0_solution = from_vertical(vertical=vertical_0, square_to_threats=square_to_threats)
    if vertical_0_solution is not None:
        already_solved_threats.update(vertical_0_solution.threats)
    vertical_1_solution = from_vertical(vertical=vertical_1, square_to_threats=square_to_threats)
    if vertical_1_solution is not None:
        already_solved_threats.update(vertical_1_solution.threats)
    lowinverse_solution = from_lowinverse(lowinverse=highinverse.lowinverse, square_to_threats=square_to_threats)
    if lowinverse_solution is not None:
        already_solved_threats.update(lowinverse_solution.threats)

    if not highinverse_threats.issubset(already_solved_threats):
        # Form the highinverse into a solution.
        squares = frozenset([
            upper_square_0,
            vertical_0.upper,
            vertical_0.lower,
            upper_square_1,
            vertical_1.upper,
            vertical_1.lower,
        ])
        return Solution(
            rule=Rule.Highinverse,
            squares=squares,
            threats=frozenset(highinverse_threats),
        )
    # If the highinverse does not have any new threats, then we don't convert
    # the Highinverse into a Solution.


def from_baseclaim(baseclaim: Baseclaim, square_to_threats) -> Solution:
    """Converts a Baseclaim into a Solution.
    Must solve at least one potential threat in order to be converted into a Solution.

    Args:
        baseclaim (Baseclaim): a Baseclaim.
        square_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if baseclaim can be converted into one. None if it can't.
    """
    threats = set()

    # Add all threats which contain the first playable square and the square above the second playable
    # square.
    square_above_second = Square(row=baseclaim.second.row - 1, col=baseclaim.second.col)
    threats.update(square_to_threats[baseclaim.first].intersection(square_to_threats[square_above_second]))

    # Add all threats which contain the second and third playable square.
    threats.update(square_to_threats[baseclaim.second].intersection(square_to_threats[baseclaim.third]))

    # If there is at least one threat:
    if threats:
        squares = frozenset([baseclaim.first, baseclaim.second, baseclaim.third, square_above_second])
        return Solution(
            rule=Rule.Baseclaim,
            squares=squares,
            threats=frozenset(threats),
            claimeven_bottom_squares=[baseclaim.second],
        )


def from_before(before: Before, square_to_threats) -> Solution:
    """Converts a Before into a Solution.
    Must solve at least one *new* potential threat in order to be converted into a Solution.
    By "new potential threat," we mean any threat that contains all successors of the empty
    squares in the Before group.

    Args:
        before (Before): a Before.
        square_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if before can be converted into one. None if it can't.
    """
    empty_squares = before.empty_squares_of_before_group()
    empty_square_successors = []
    for square in empty_squares:
        empty_square_successors.append(Square(row=square.row - 1, col=square.col))

    threats = square_to_threats[empty_square_successors[0]]
    for square in empty_square_successors[1:]:
        threats = threats.intersection(square_to_threats[square])

    # If there is at least one threat that contains all direct successors of all empty squares in the Before group:
    if threats:
        squares = set(empty_squares)

        for vertical in before.verticals:
            # Add all squares part of Verticals which are part of the Before.
            squares.add(vertical.upper)
            squares.add(vertical.lower)
            # Add all threats refuted by Verticals which are part of the Before.
            threats.update(from_vertical(vertical, square_to_threats).threats)

        claimeven_bottom_squares = []
        for claimeven in before.claimevens:
            # Add all squares part of Claimevens which are part of the Before.
            squares.add(claimeven.upper)
            squares.add(claimeven.lower)
            claimeven_bottom_squares.append(claimeven.lower)
            # Add all threats refuted by Claimevens which are part of the Before.
            threats.update(from_claimeven(claimeven, square_to_threats).threats)

        return Solution(
            rule=Rule.Before,
            squares=frozenset(squares),
            threats=frozenset(threats),
            claimeven_bottom_squares=claimeven_bottom_squares,
        )


def from_specialbefore(specialbefore: Specialbefore, square_to_threats) -> Solution:
    """Converts a Specialbefore into a Solution.
    Must solve at least one *new* potential threat in order to be converted into a Solution.
    By "new potential threat," we mean threats that meet either of the following conditions:
    1. Threats that contain the external directly playable square and
       all successors of empty squares of the Specialbefore.
    2. Threats that contain the internal directly playable square and external directly playable square
       of the Specialbefore.

    Args:
        specialbefore (Specialbefore): a Specialbefore.
        square_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if before can be converted into one. None if it can't.
    """
    # Find all threats that contain the external directly playable square and
    # all successors of empty squares of the Specialbefore.
    external_and_successor_threats = square_to_threats[specialbefore.external_directly_playable_square]
    empty_squares = specialbefore.before.empty_squares_of_before_group()
    for square in empty_squares:
        direct_successor = Square(row=square.row - 1, col=square.col)
        external_and_successor_threats = external_and_successor_threats.intersection(
            square_to_threats[direct_successor])

    if external_and_successor_threats:
        # Find all threats that contain the internal directly playable square and
        # external directly playable square of the Specialbefore.
        # Essentially, reproducing the threats refuted by a Baseinverse.
        sq1 = specialbefore.internal_directly_playable_square
        sq2 = specialbefore.external_directly_playable_square
        directly_playable_squares_threats = square_to_threats[sq1].intersection(square_to_threats[sq2])

        # The union of external_and_successor_threats and directly_playable_squares_threats are all
        # new threats that this Specialbefore refutes.
        threats = external_and_successor_threats.union(directly_playable_squares_threats)

        # The Specialbefore Solution includes all squares and threats that the Before Solution has.
        before_solution = from_before(before=specialbefore.before, square_to_threats=square_to_threats)
        return Solution(
            rule=Rule.Specialbefore,
            squares=frozenset(before_solution.squares.union([specialbefore.external_directly_playable_square])),
            threats=frozenset(before_solution.threats.union(threats)),
            claimeven_bottom_squares=before_solution.claimeven_bottom_squares,
        )
