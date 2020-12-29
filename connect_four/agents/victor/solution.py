from collections import namedtuple

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


def from_claimeven(claimeven: Claimeven) -> Solution:
    pass


def from_baseinverse(baseinverse: Baseinverse) -> Solution:
    pass


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
