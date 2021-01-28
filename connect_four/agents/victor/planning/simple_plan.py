from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Aftereven
from connect_four.agents.victor.rules import Before
from connect_four.agents.victor.rules import Specialbefore


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
        responses = self.responses.copy()
        responses.update(simple_plan.responses)
        availabilities = self.availabilities.union(simple_plan.availabilities)
        return SimplePlan(responses=responses, availabilities=availabilities)

    def add_responses(self, responses):
        pass

    def add_availabilities(self, availabilities):
        return SimplePlan(
            self.responses,
            self.availabilities.union(set(availabilities)),
        )


class SimplePlanBuilder:
    def __init__(self, plans=None):
        if plans is None:
            plans = []
        self.plans = plans.copy()

    def add(self, plan):
        self.plans.append(plan)

    def build(self):
        responses = dict()
        availabilities = set()
        for plan in self.plans:
            if isinstance(plan, SimplePlan):
                responses.update(plan.responses)
                availabilities.update(plan.availabilities)
            elif isinstance(plan, Square):
                availabilities.add(plan)
            else:  # plan must be a response
                responses.update(plan)
        return SimplePlan(responses=responses, availabilities=availabilities)


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


def from_before(before: Before) -> SimplePlan:
    builder = SimplePlanBuilder()
    for vertical in before.verticals:
        builder.add(plan=from_vertical(vertical=vertical))
    for claimeven in before.claimevens:
        builder.add(plan=from_claimeven(claimeven=claimeven))
    return builder.build()


def from_specialbefore(specialbefore: Specialbefore) -> SimplePlan:
    builder = SimplePlanBuilder()
    builder.add(
        plan=from_baseinverse(
            baseinverse=Baseinverse(
                playable1=specialbefore.internal_directly_playable_square,
                playable2=specialbefore.external_directly_playable_square),
        ),
    )
    for vertical in specialbefore.before.verticals:
        if vertical != specialbefore.unused_vertical():
            builder.add(plan=from_vertical(vertical=vertical))
    for claimeven in specialbefore.before.claimevens:
        builder.add(plan=from_claimeven(claimeven=claimeven))
    return builder.build()
