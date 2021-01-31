from connect_four.agents.victor.game import Square

from connect_four.agents.victor.planning import simple_plan

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Aftereven


class Plan:
    def __init__(self, rule_applications, availabilities=None, directly_playable_squares=None):
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
            directly_playable_squares (Set<Square>): a set of directly playable Squares.
        """
        if availabilities is None:
            availabilities = set()
        if directly_playable_squares is None:
            directly_playable_squares = set()

        self.responses = dict()
        self.availabilities = set(availabilities)
        self.directly_playable_squares = set(directly_playable_squares)

        for application in rule_applications:
            if isinstance(application, Claimeven):
                plan = simple_plan.from_claimeven(claimeven=application)
            elif isinstance(application, Baseinverse):
                plan = simple_plan.from_baseinverse(baseinverse=application)
            elif isinstance(application, Vertical):
                plan = simple_plan.from_vertical(vertical=application)
            elif isinstance(application, Aftereven):
                plan = simple_plan.from_aftereven(aftereven=application)
            else:
                raise TypeError("unsupported application type", application.__class__.__name__)

            self.responses.update(plan.responses)
            self.availabilities.update(plan.availabilities)

    def __eq__(self, other):
        if isinstance(other, Plan):
            return self.responses == other.responses and self.availabilities == other.availabilities
        return False

    def execute(self, square: Square) -> Square:
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

        Returns:
            response (Square): a Square in directly_playable_squares.
        """
        self._update_directly_playable_squares(square=square)
        print("self.directly_playable_squares =", self.directly_playable_squares)

        if square in self.responses:
            response = self.responses[square]

            # square has been taken so it is no longer available.
            if square in self.availabilities:
                self.availabilities.remove(square)

            # response is exactly a Square.
            if isinstance(response, Square):
                self.responses.pop(square)
                self._update_directly_playable_squares(square=response)
                return response

            # else: response must be a Fork.

        # Remove square from availabilities.
        self.availabilities.remove(square)
        # Select an arbitrary, available, directly playable Square.
        response = self.availabilities.intersection(self.directly_playable_squares).pop()

        # Remove response from responses if applicable.
        if response in self.responses:
            self.responses.pop(response)
        # Remove response from availabilities.
        self.availabilities.remove(response)

        self._update_directly_playable_squares(square=response)
        return response

    def _update_directly_playable_squares(self, square: Square):
        if square not in self.directly_playable_squares:
            raise ValueError("square", square, "not in directly playable squares:", self.directly_playable_squares)

        self.directly_playable_squares.remove(square)

        if square.row != 0:
            # If square is not in the top row, add the Square above it.
            self.directly_playable_squares.add(Square(row=square.row - 1, col=square.col))
