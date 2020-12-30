from collections import namedtuple

from connect_four.agents.victor import Rule

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


def from_vertical(vertical: Vertical) -> Solution:
    pass


def from_aftereven(aftereven: Aftereven) -> Solution:
    pass


def from_lowinverse(lowinverse: Lowinverse) -> Solution:
    pass


def from_highinverse(highinverse: Highinverse) -> Solution:
    pass


def from_baseclaim(baseclaim: Baseclaim) -> Solution:
    pass


def from_before(before: Before) -> Solution:
    pass


def from_specialbefore(specialbefore: Specialbefore) -> Solution:
    pass
