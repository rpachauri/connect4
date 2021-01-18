from collections import namedtuple

from connect_four.agents.victor.rules import Claimeven

Plan = namedtuple("Plan", ["follow_up_plans"])


def from_claimeven(claimeven: Claimeven):
    return Plan(
        follow_up_plans={
            claimeven.lower: claimeven.upper,
        },
    )
