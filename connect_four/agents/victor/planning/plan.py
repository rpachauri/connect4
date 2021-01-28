from connect_four.agents.victor.game import Square

from connect_four.agents.victor.planning import simple_plan

from connect_four.agents.victor.rules import Claimeven


class Plan:
    def __init__(self, rule_applications):
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
        """
        self.responses = dict()
        self.availabilities = set()

        for application in rule_applications:
            if isinstance(application, Claimeven):
                claimeven_simple_plan = simple_plan.from_claimeven(claimeven=application)
                self.responses.update(claimeven_simple_plan.responses)
                self.availabilities.update(claimeven_simple_plan.availabilities)

    def __eq__(self, other):
        if isinstance(other, Plan):
            return self.responses == other.responses and self.availabilities == other.availabilities
        return False

    def execute(self, square: Square, directly_playable_squares) -> Square:
        """Executes this Plan by responding to square.

        Raises:
            ValueError: If square is not in directly_playable_squares.
            KeyError: If this Plan doesn't have a known response for square and square is not known to be available.

        Modifies:
            this:
                1. If square forces a Square in this Plan, this Plan will no longer store that response.
                2. If square forces a Fork in this Plan, this Plan will remove any references to the Fork and
                    add any SimplePlans part of the chosen Branch.
                3. If square is an available square, selects an available directly playable Square.

        Args:
            square (Square): a directly playable Square.
            directly_playable_squares (iterable<Square>): an iterable of directly playable Squares.

        Returns:
            response (Square): a Square in directly_playable_squares or directly above square. response != square.
        """
        if square not in directly_playable_squares:
            raise ValueError("square", square, "not in directly playable squares:", directly_playable_squares)
        if square in self.responses:
            response = self.responses[square]

            # response is exactly a Square.
            if isinstance(response, Square):
                self.responses.pop(square)
                return response

            # else: response must be a Fork.
        pass  # TODO pick a square from self.availabilities.
