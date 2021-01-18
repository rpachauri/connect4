from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse


class Plan:
    def __init__(self, responses=None):
        if responses is None:
            responses = dict()
        self.responses = responses

    def __eq__(self, other):
        if isinstance(other, Plan):
            return self.responses == other.responses
        return False

    def execute(self, square: Square) -> Square:
        if square in self.responses:
            # Find the appropriate response for square and remove it from the plan.
            response = self.responses[square]
            self.responses.pop(square)

            # Since the response is being executed, we no longer need a response for it.
            if response in self.responses:
                self.responses.pop(response)
            return response


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