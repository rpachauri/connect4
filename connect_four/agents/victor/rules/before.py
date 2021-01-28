from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Threat
from connect_four.agents.victor.game import ThreatDirection

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Vertical


class Before:
    def __init__(self, threat: Threat, verticals, claimevens):
        """Initializes a Before instance.

        Args:
            threat (Threat): a Threat representing the Before group.
            verticals (iterable<Vertical>): an iterable of Verticals which are part of the Before.
            claimevens (iterable<Vertical>): an iterable of Claimevens which are part of the Before.
        """
        self.threat = threat
        self.verticals = frozenset(verticals)
        self.claimevens = frozenset(claimevens)

    def __eq__(self, other):
        if isinstance(other, Before):
            return (self.threat == other.threat and
                    self.verticals == other.verticals and
                    self.claimevens == other.claimevens)

    def __hash__(self):
        return self.threat.__hash__() * 41 + self.verticals.__hash__() * 31 + self.claimevens.__hash__()

    def empty_squares_of_before_group(self):
        """Returns the empty squares of the Before group of this Before.

        Returns:
            empty_squares (Set<Square>): The empty squares of the Before group of this Before.
        """
        empty_squares = set()

        for vertical in self.verticals:
            if vertical.upper in self.threat.squares:
                empty_squares.add(vertical.upper)
            else:
                empty_squares.add(vertical.lower)

        for claimeven in self.claimevens:
            # claimeven.upper should be an empty square part of the Before group by definition.
            # Otherwise, something is wrong.
            empty_squares.add(claimeven.upper)

        return frozenset(empty_squares)


def find_all_befores(board: Board, threats):
    """find_all_befores takes a Board and an iterable of Threats and returns an iterable of Befores for the Board.

    Args:
        board (Board): a Board instance.
        # TODO rename to opponent_threats to be more clear to clients.
        threats (iterable<Threat>): an iterable of Threats belonging to the opponent of the player to move on board.

    Returns:
        befores (iterable<Before>): an iterable of Befores for board.
    """
    befores = set()

    for threat in threats:
        # Skip all Vertical threats.
        if threat.direction == ThreatDirection.vertical:
            continue

        # empty_squares is the set of all squares that belong to threat and are empty.
        # If there is a single square that belongs in the uppermost row of board, then len(empty_squares) == 0.
        empty_squares = empty_squares_of_before_group(board, threat)

        if empty_squares:  # Only create variations if empty_squares has at least one square.
            # Add all Before variations with threat as the Before group to befores.
            add_before_variations(board, befores, threat, empty_squares, [], [])

    return befores


def empty_squares_of_before_group(board: Board, threat: Threat):
    """Retrieves the empty squares of a Before group if the given threat meets the conditions of a Before group.
    Returns an empty list if the threat does not meet the conditions.

    Args:
        board (Board): a Board instance.
        threat (Threat): a possible Before group.

    Returns:
        empty_squares (list<Square>):
            TODO: Should be -> If square.row == 0 for every square in threat.squares:
            If there exists a square with square.row == 0 in threat:
                returns []
            Otherwise:
                returns a list of empty Squares in threat.
    """
    empty_squares = []
    for square in threat.squares:
        if square.row == 0:
            return []
        if board.is_empty(square):
            empty_squares.append(square)
    return empty_squares


def add_before_variations(board: Board, befores, threat: Threat, empty_squares, verticals, claimevens):
    """Adds all Before variations with threat as the Before group to befores.

    Args:
        board (Board): a Board instance.
        befores (set<Before>): a set of Befores we have accumulated so far for board.
            Any new Befores we find with threat as the Before group will be added to befores.
        threat (Threat): the Before group. Any new Befores we add to befores must use threat as their Before group.
        empty_squares (list<Square>): a list of empty Squares in threat.
        verticals (set<Vertical>): a set of Verticals which are part of the Before we are building.
        claimevens (set<Claimeven>): a set of Claimevens which are part of the Before we are building.

    Returns:

    """
    # This is a Recursive Backtracking algorithm.
    # Base Case.
    if not empty_squares:
        if len(verticals) > 0:
            # Only add the Before if there is at least one Vertical; otherwise, an Aftereven is better.
            befores.add(Before(threat=threat, verticals=verticals, claimevens=claimevens))
        return

    # Recursive Case.
    square = empty_squares.pop()  # Remove a square from empty_squares.
    square_below = Square(row=square.row + 1, col=square.col)
    square_above = Square(row=square.row - 1, col=square.col)

    # Whether square is odd or even, we can always try to create a Vertical with square as the lower square.
    if board.is_valid(square_above):
        vertical = Vertical(upper=square_above, lower=square)
        # Choose.
        verticals.append(vertical)
        # Recurse.
        add_before_variations(board, befores, threat, empty_squares, verticals, claimevens)
        # Unchoose.
        verticals.remove(vertical)

    # Depending on whether square is odd or even, we try to create a Vertical or Claimeven respectively.
    if square.row % 2 == 1:  # square is odd.
        if board.is_valid(square_below) and board.is_empty(square_below):
            # Create a Vertical with square as the upper square.
            vertical = Vertical(upper=square, lower=square_below)
            # Choose.
            verticals.append(vertical)
            # Recurse.
            add_before_variations(board, befores, threat, empty_squares, verticals, claimevens)
            # Unchoose.
            verticals.remove(vertical)
    else:  # square is even.
        # Since square is even, we are guaranteed that square_below is valid
        # because board must have an even number of rows.
        if board.is_empty(square_below):
            # Create a Claimeven with square as the upper square.
            claimeven = Claimeven(upper=square, lower=square_below)
            # Choose.
            claimevens.append(claimeven)
            # Recurse.
            add_before_variations(board, befores, threat, empty_squares, verticals, claimevens)
            # Unchoose.
            claimevens.remove(claimeven)

    empty_squares.append(square)
