from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Aftereven


class SimplePlan:
    def __init__(self, responses=None, availabilities=None):
        if responses is None:
            responses = dict()
        if availabilities is None:
            availabilities = set()
        self.responses = responses
        self.availabilities = availabilities

    def __eq__(self, other):
        if isinstance(other, SimplePlan):
            return self.responses == other.responses and self.availabilities == other.availabilities
        return False

    def merge(self, simple_plan):
        pass

    def add_responses(self, responses):
        pass

    def add_availability(self, availability):
        pass


class SimplePlanBuilder:
    def __init__(self, plans=None):
        if plans is None:
            plans = []
        self.plans = plans.copy()

    def add(self, plan):
        pass

    def build(self):
        pass


def from_claimeven(claimeven: Claimeven) -> SimplePlan:
    return SimplePlan(
        responses={
            claimeven.lower: claimeven.upper,
        },
    )


def from_baseinverse(baseinverse: Baseinverse) -> SimplePlan:
    square0, square1 = tuple(baseinverse.squares)
    return SimplePlan(
        responses={
            square0: square1,
            square1: square0,
        }
    )


def from_vertical(vertical: Vertical) -> SimplePlan:
    return SimplePlan(
        responses={
            vertical.lower: vertical.upper,
        },
        availabilities={vertical.lower},
    )


def from_aftereven(aftereven: Aftereven) -> SimplePlan:
    responses = dict()
    for claimeven in aftereven.claimevens:
        responses[claimeven.lower] = claimeven.upper
    return SimplePlan(responses=responses)
