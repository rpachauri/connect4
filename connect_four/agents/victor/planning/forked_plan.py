from collections import namedtuple

from connect_four.agents.victor.rules import Lowinverse

from connect_four.agents.victor.planning.simple_plan import from_vertical


Branch = namedtuple("Branch", ["forced_square", "simple_plan"])
Fork = namedtuple("Fork", ["branches"])


def from_lowinverse(lowinverse: Lowinverse) -> Fork:
    vertical0, vertical1 = tuple(lowinverse.verticals)
    return Fork(
        branches={
            vertical0.lower: Branch(
                forced_square=vertical0.upper,
                simple_plan=from_vertical(vertical1),
            ),
            vertical1.lower: Branch(
                forced_square=vertical1.upper,
                simple_plan=from_vertical(vertical0),
            ),
        }
    )
