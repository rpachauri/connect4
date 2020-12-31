from collections import namedtuple

from connect_four.agents.victor import Rule
from connect_four.agents.victor import Square

from connect_four.agents.victor import Claimeven
from connect_four.agents.victor import Baseinverse
from connect_four.agents.victor import Vertical
from connect_four.agents.victor import Aftereven
from connect_four.agents.victor import Lowinverse
from connect_four.agents.victor import Highinverse
from connect_four.agents.victor import Baseclaim
from connect_four.agents.victor import Before
from connect_four.agents.victor import Specialbefore

"""A Solution is an application of a Rule that refutes at least one threat.

Two Solutions may or may not work together depending on which squares each
consists of and which rule they are an application of.
"""
Solution = namedtuple("Solution", ["rule", "squares", "threats"])


def from_claimeven(claimeven: Claimeven, squares_to_threats) -> Solution:
    """Converts a Claimeven into a Solution.
    Must solve at least one potential threat in order to be converted into a Solution.

    Args:
        claimeven (Claimeven): a Claimeven.
        squares_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if claimeven can be converted into one. None if it can't.
    """
    threats = squares_to_threats[claimeven.upper]
    if threats:  # len(threats) > 0
        squares = frozenset([claimeven.upper, claimeven.lower])
        return Solution(rule=Rule.Claimeven, squares=squares, threats=threats)


def from_baseinverse(baseinverse: Baseinverse, squares_to_threats) -> Solution:
    """Converts a Baseinverse into a Solution.
    Must solve at least one potential threat in order to be converted into a Solution.

    Args:
        baseinverse (Baseinverse): a Baseinverse.
        squares_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if baseinverse can be converted into one. None if it can't.
    """
    square1, square2 = tuple(baseinverse.squares)
    threats1, threats2 = squares_to_threats[square1], squares_to_threats[square2]
    threats_intersection = threats1.intersection(threats2)
    if threats_intersection:
        squares = frozenset([square1, square2])
        return Solution(rule=Rule.Baseinverse, squares=squares, threats=threats_intersection)


def from_vertical(vertical: Vertical, squares_to_threats) -> Solution:
    """Converts a Vertical into a Solution.
    Must solve at least one potential threat in order to be converted into a Solution.

    Args:
        vertical (Vertical): a Vertical.
        squares_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if vertical can be converted into one. None if it can't.
    """
    upper_threats, lower_threats = squares_to_threats[vertical.upper], squares_to_threats[vertical.lower]
    threats_intersection = upper_threats.intersection(lower_threats)
    if threats_intersection:
        squares = frozenset([vertical.upper, vertical.lower])
        return Solution(rule=Rule.Vertical, squares=squares, threats=threats_intersection)


def from_aftereven(aftereven: Aftereven, squares_to_threats) -> Solution:
    """Converts an Aftereven into a Solution.
    Must solve at least one *new* potential threat in order to be converted into a Solution.
    By "new potential threat," we mean any threat that isn't already solved by one of the Claimevens
    which are part of the Aftereven.

    Args:
        aftereven (Aftereven): an Aftereven.
        squares_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
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
        squares_to_threats=squares_to_threats,
    )

    # Aftereven should only be converted into a Solution if it refutes new threats.
    if threats:
        squares_involved = list(aftereven.threat.squares)
        for claimeven in aftereven.claimevens:
            claimeven_solution = from_claimeven(claimeven, squares_to_threats)
            threats.update(claimeven_solution.threats)
            squares_involved.append(claimeven.lower)

        return Solution(
            rule=Rule.Aftereven,
            squares=frozenset(squares_involved),
            threats=frozenset(threats),
        )


def add_new_threats_from_aftereven(threats, empty_squares_of_aftereven, threatening_squares, squares_to_threats):
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
        squares_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        None
    """
    # Base case.
    if not empty_squares_of_aftereven:
        new_threats_to_add = squares_to_threats[threatening_squares[0]]
        for square in threatening_squares[1:]:
            new_threats_to_add = new_threats_to_add.intersection(squares_to_threats[square])
        threats.update(new_threats_to_add)
        return

    # Recursive Case.
    square = empty_squares_of_aftereven.pop()
    for row in range(square.row - 1, -1, -1):
        square_above = Square(row=row, col=square.col)
        # Choose.
        threatening_squares.append(square_above)
        # Recurse.
        add_new_threats_from_aftereven(threats, empty_squares_of_aftereven, threatening_squares, squares_to_threats)
        # Unchoose.
        threatening_squares.remove(square_above)
    empty_squares_of_aftereven.append(square)


def from_lowinverse(lowinverse: Lowinverse, squares_to_threats) -> Solution:
    """Converts a Lowinverse into a Solution.
    Must solve at least one *new* potential threat in order to be converted into a Solution.
    By "new potential threat," we mean any threat that isn't already solved by one of the Verticals
    which are part of the Lowinverse.

    Args:
        lowinverse (Lowinverse): a Lowinverse.
        squares_to_threats (Map<Square, Set<Threat>>): A dictionary mapping each
            Square to all Threats that contain that Square.

    Returns:
        solution (Solution): a Solution if lowinverse can be converted into one. None if it can't.
    """
    verticals_as_list = list(lowinverse.verticals)
    vertical_0, vertical_1 = verticals_as_list[0], verticals_as_list[1]
    threats = squares_to_threats[vertical_0.upper].intersection(squares_to_threats[vertical_1.upper])

    # Lowinverse should only be converted into a Solution if it refutes new threats.
    if threats:
        squares = [vertical_0.upper, vertical_0.lower, vertical_1.upper, vertical_1.lower]

        vertical_0_threats = from_vertical(vertical_0, squares_to_threats).threats
        vertical_1_threats = from_vertical(vertical_1, squares_to_threats).threats
        threats.update(vertical_0_threats)
        threats.update(vertical_1_threats)

        return Solution(
            rule=Rule.Lowinverse,
            squares=frozenset(squares),
            threats=frozenset(threats),
        )


def from_highinverse(highinverse: Highinverse) -> Solution:
    pass


def from_baseclaim(baseclaim: Baseclaim) -> Solution:
    pass


def from_before(before: Before) -> Solution:
    pass


def from_specialbefore(specialbefore: Specialbefore) -> Solution:
    pass
