from connect_four.agents.victor.game import Square

from connect_four.agents.victor.planning import simple_plan

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical


class Plan:
    def __init__(self, rule_applications, availabilities=None):
        """Initializes a Plan instance.

        Requires:
            1. Every application_1 in rule_applications must be able to be combined with every other application_2 in
                rule_applications.

        Assumptions:
            1. Makes an assumption that together, all applications in rule_applications can be used to respond to
                any move the opponent makes until the end of the game.

        Args:
            rule_applications (Iterable): rule_applications is an iterable of Rule applications:
                (Claimeven, Baseinverse, etc.).
            availabilities (Set<Square>): a set of available Squares.
        """
        if availabilities is None:
            availabilities = set()

        self.responses = dict()
        self.availabilities = set(availabilities)

        for application in rule_applications:
            if isinstance(application, Claimeven):
                plan = simple_plan.from_claimeven(claimeven=application)
            elif isinstance(application, Baseinverse):
                plan = simple_plan.from_baseinverse(baseinverse=application)
            elif isinstance(application, Vertical):
                plan = simple_plan.from_vertical(vertical=application)
            else:
                raise TypeError("unsupported application type", application.__class__.__name__)

            self.responses.update(plan.responses)
            self.availabilities.update(plan.availabilities)

    def __eq__(self, other):
        if isinstance(other, Plan):
            return self.responses == other.responses and self.availabilities == other.availabilities
        return False

    def execute(self, square: Square, directly_playable_squares) -> Square:
        """Executes this Plan by responding to square.

        Raises:
            KeyError: If this Plan doesn't have a known response for square and square is not known to be available.

        Modifies:
            this:
                1. If square forces a Square in this Plan, this Plan will no longer store that response.
                2. If square forces a Fork in this Plan, this Plan will remove any references to the Fork and
                    add any SimplePlans part of the chosen Branch.
                3. If square is an available square, selects an available directly playable Square.

        Args:
            square (Square): a directly playable Square.
            directly_playable_squares (Set<Square>): an iterable of directly playable Squares. If square is not in the
                top row, it must contain the Square above square.

        Returns:
            response (Square): a Square in directly_playable_squares.
        """
        if square in self.responses:
            response = self.responses[square]

            # square has been taken so it is no longer available.
            if square in self.availabilities:
                self.availabilities.remove(square)

            # response is exactly a Square.
            if isinstance(response, Square):
                self.responses.pop(square)
                return response

            # else: response must be a Fork.

        # Remove square from availabilities.
        self.availabilities.remove(square)
        # Select an arbitrary, available, directly playable Square.
        response = self.availabilities.intersection(directly_playable_squares).pop()

        # Remove response from responses if applicable.
        if response in self.responses:
            self.responses.pop(response)
        # Remove response from availabilities.
        self.availabilities.remove(response)

        return response
