from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Aftereven


class Plan:
    def __init__(self, responses=None, availabilities=None):
        if responses is None:
            responses = dict()
        if availabilities is None:
            availabilities = set()
        self.responses = responses
        self.availabilities = availabilities

    def __eq__(self, other):
        if isinstance(other, Plan):
            return self.responses == other.responses and self.availabilities == other.availabilities
        return False

    def __hash__(self):
        return self.responses.__hash__() * 97 + self.availabilities.__hash__() * 53

    def execute(self, square: Square) -> Square:
        if square in self.responses:
            # Find the appropriate response for square and remove it from the plan.
            response = self.responses[square]
            self.responses.pop(square)

            # Since the response is being executed, we no longer need a response for it.
            if response in self.responses:
                self.responses.pop(response)
            return response
        # TODO pick a square from self.availabilities.


def from_claimeven(claimeven: Claimeven):
    return Plan(
        responses={
            claimeven.lower: claimeven.upper,
        },
    )


def from_baseinverse(baseinverse: Baseinverse):
    square0, square1 = tuple(baseinverse.squares)
    return Plan(
        responses={
            square0: square1,
            square1: square0,
        }
    )


def from_vertical(vertical: Vertical):
    return Plan(
        responses={
            vertical.lower: vertical.upper,
        },
        availabilities={vertical.lower},
    )


def from_aftereven(aftereven: Aftereven):
    responses = dict()
    for claimeven in aftereven.claimevens:
        responses[claimeven.lower] = claimeven.upper
    return Plan(responses=responses)