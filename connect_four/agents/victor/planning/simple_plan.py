from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Aftereven
from connect_four.agents.victor.rules import Before
from connect_four.agents.victor.rules import Specialbefore

from connect_four.agents.victor.threat_hunter import Threat
from connect_four.agents.victor.threat_hunter import ThreatCombination


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
        availabilities={vertical.lower, vertical.upper},
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


def from_odd_threat(odd_threat: Threat, directly_playable_square: Square) -> SimplePlan:
    builder = SimplePlanBuilder()

    # Directly playable odd square in odd threat column is an availability.
    if directly_playable_square.row % 2 == 1:
        builder.add(directly_playable_square)
        lowest_even_row = directly_playable_square.row - 1
    else:
        lowest_even_row = directly_playable_square.row

    # All even squares force the square above it in the odd threat column.
    # Only need to add the even squares below the empty square of the odd threat.
    for even_row in range(lowest_even_row, odd_threat.empty_square.row, -2):
        even_square = Square(row=even_row, col=odd_threat.empty_square.col)
        odd_square = Square(row=even_row - 1, col=odd_threat.empty_square.col)
        builder.add({even_square: odd_square})

    return builder.build()


def from_threat_combination(
        threat_combination: ThreatCombination,
        directly_playable_crossing_square: Square,
        directly_playable_stacked_square: Square) -> SimplePlan:
    builder = SimplePlanBuilder()

    # Directly playable odd square in crossing column is an availability.
    if directly_playable_crossing_square.row % 2 == 1:
        builder.add(directly_playable_crossing_square)
        lowest_even_row = directly_playable_crossing_square.row - 1
    else:
        lowest_even_row = directly_playable_crossing_square.row

    # All even squares force the square above it in the crossing column.
    for even_row in range(lowest_even_row, 0, -2):
        even_square = Square(row=even_row, col=threat_combination.crossing_column())
        odd_square = Square(row=even_row - 1, col=threat_combination.crossing_column())
        builder.add({even_square: odd_square})

    # Top even square in crossing column is an availability.
    builder.add(Square(row=0, col=threat_combination.crossing_column()))

    # All squares force the square above it in the stacked column.
    for upper_row in range(directly_playable_stacked_square.row):
        upper_square = Square(row=upper_row, col=threat_combination.stacked_column())
        lower_square = Square(row=upper_row + 1, col=threat_combination.stacked_column())
        builder.add({lower_square: upper_square})

    return builder.build()
