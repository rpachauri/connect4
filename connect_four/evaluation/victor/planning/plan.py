from connect_four.game import Square

from connect_four.evaluation.victor.rules import Claimeven
from connect_four.evaluation.victor.rules import Baseinverse
from connect_four.evaluation.victor.rules import Vertical
from connect_four.evaluation.victor.rules import Aftereven
from connect_four.evaluation.victor.rules import Lowinverse
from connect_four.evaluation.victor.rules import Highinverse
from connect_four.evaluation.victor.rules import Baseclaim
from connect_four.evaluation.victor.rules import Before
from connect_four.evaluation.victor.rules import Specialbefore

from connect_four.evaluation.victor.threat_hunter import Threat
from connect_four.evaluation.victor.threat_hunter import ThreatCombination

from connect_four.evaluation.victor.planning import simple_plan
from connect_four.evaluation.victor.planning import forked_plan


class Plan:
    def __init__(self, rule_applications,
                 odd_group_guarantor=None,
                 availabilities=None,
                 directly_playable_squares=None):
        """Initializes a Plan instance.

        Requires:
            1. Every application_1 in rule_applications must be able to be combined with every other application_2 in
                rule_applications.

        Assumptions:
            1. Makes an assumption that together, all applications in rule_applications can be used to respond to
                any move the opponent makes until the end of the board.

        Args:
            rule_applications (Iterable): rule_applications is an iterable of Rule applications:
                (Claimeven, Baseinverse, etc.).
            odd_group_guarantor (Threat | ThreatCombination): A Threat or ThreatCombination for White.
            availabilities (Set<Square>): a set of available Squares.
                availabilities should be disjoint from the set of squares from rule_applications.
            directly_playable_squares (Set<Square>): a set of directly playable Squares.
        """
        if availabilities is None:
            availabilities = set()
        if directly_playable_squares is None:
            directly_playable_squares = set()

        self.forcing_to_forced = dict()
        self.availabilities = set(availabilities)
        self.forks = []
        self.directly_playable_squares = set(directly_playable_squares)
        self.stacked_column = -1

        for application in rule_applications:
            if isinstance(application, Claimeven):
                self._add(plan=simple_plan.from_claimeven(claimeven=application))
            elif isinstance(application, Baseinverse):
                self._add(plan=simple_plan.from_baseinverse(baseinverse=application))
            elif isinstance(application, Vertical):
                self._add(plan=simple_plan.from_vertical(vertical=application))
            elif isinstance(application, Aftereven):
                self._add(plan=simple_plan.from_aftereven(aftereven=application))
            elif isinstance(application, Lowinverse):
                self.forks.append(forked_plan.from_lowinverse(lowinverse=application))
            elif isinstance(application, Highinverse):
                self.forks.append(forked_plan.from_highinverse(highinverse=application))
            elif isinstance(application, Baseclaim):
                self.forks.append(forked_plan.from_baseclaim(baseclaim=application))
            elif isinstance(application, Before):
                self._add(plan=simple_plan.from_before(before=application))
            elif isinstance(application, Specialbefore):
                self._add(plan=simple_plan.from_specialbefore(specialbefore=application))
            else:
                raise TypeError("unsupported application type", application.__class__.__name__)

        if isinstance(odd_group_guarantor, Threat):
            self._add(plan=simple_plan.from_odd_threat(
                odd_threat=odd_group_guarantor,
                directly_playable_square=self._directly_playable_square(odd_group_guarantor.empty_square.col),
            ))
        elif isinstance(odd_group_guarantor, ThreatCombination):
            self._add(plan=simple_plan.from_threat_combination(
                threat_combination=odd_group_guarantor,
                directly_playable_crossing_square=self._directly_playable_square(odd_group_guarantor.crossing_column()),
                directly_playable_stacked_square=self._directly_playable_square(odd_group_guarantor.stacked_column()),
            ))
            self.stacked_column = odd_group_guarantor.stacked_column()

    def _directly_playable_square(self, col) -> Square:
        for square in self.directly_playable_squares:
            if square.col == col:
                return square
        raise ValueError("col", col, "not found in:", self.directly_playable_squares)

    def __eq__(self, other):
        if isinstance(other, Plan):
            return self.forcing_to_forced == other.forcing_to_forced and self.availabilities == other.availabilities
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
            square (Square): a directly playable Square representing the opponent's move.

        Returns:
            response (Square): a Square in directly_playable_squares.
        """
        # Find if square belongs to a Fork.
        fork = self._find_fork(square)
        # If square belongs to a Fork, implement the SimplePlan using square as the branching square.
        if fork is not None:
            self._add(plan=fork.branches[square])
            self.forks.remove(fork)

        # Find an appropriate response to square, updating self.directly_playable_squares in the process.
        self._play(square=square)
        response = self._find_response(square=square)
        self._play(square=response)

        # Remove square and response from self.forcing_to_forced and self.availabilities as applicable.
        self._expire(square=square)
        self._expire(square=response)

        return response

    def _find_fork(self, square: Square):
        """Find a fork that contains square if one exists for this Plan.

        Args:
            square (Square): a Square representing the opponent's move.

        Returns:
            fork (Fork): a Fork that has square in one of its branches. None if no Fork exists for this plan.
        """
        for fork in self.forks:
            if square in fork.branches:
                return fork

    def _add(self, plan: simple_plan.SimplePlan):
        """Adds a SimplePlan to this Plan.

        Args:
            plan (SimplePlan): a SimplePlan to add to this Plan.
        """
        self.forcing_to_forced.update(plan.responses)
        self.availabilities.update(plan.availabilities)

    def _find_response(self, square: Square):
        """Finds a appropriate response to square according to this Plan.

        Args:
            square (Square): a Square representing the opponent's move.

        Returns:
            response (Square): a Square representing the player's move.
        """
        if square in self.forcing_to_forced:
            return self.forcing_to_forced[square]

        directly_playable_available_squares = self.availabilities.intersection(
            self.directly_playable_squares).difference({square})
        if len(directly_playable_available_squares) != 0:
            return directly_playable_available_squares.pop()

        # White has the option of resorting to the stacked column if there are no other availabilities.
        return self._directly_playable_square(self.stacked_column)

    def _play(self, square: Square):
        """Internally "play" square and update Plan accordingly.

        Args:
            square (Square): a Square that should be directly playable.

        Raises:
            ValueError: if square is not directly playable.
        """
        # Validate that square is in self.directly_playable_squares.
        if square not in self.directly_playable_squares:
            raise ValueError("square", square, "not in directly playable squares:", self.directly_playable_squares)

        # Remove square from self.directly_playable_squares.
        self.directly_playable_squares.remove(square)

        # If square is not in the top row, add the Square above it.
        if square.row != 0:
            self.directly_playable_squares.add(Square(row=square.row - 1, col=square.col))

    def _expire(self, square: Square):
        """Removes square from self.forcing_to_forced and self.availabilities if present.

        Args:
            square (Square): a Square to expire.
        """
        # Remove square from self.forcing_to_forced if applicable.
        if square in self.forcing_to_forced:
            self.forcing_to_forced.pop(square)

        # Remove square from self.availabilities if applicable.
        if square in self.availabilities:
            self.availabilities.remove(square)
