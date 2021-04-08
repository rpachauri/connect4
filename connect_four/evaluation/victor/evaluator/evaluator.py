"""
Note that in this module, we use the term "Group" and "Problem" interchangeably.
"""
from collections import namedtuple
from typing import Dict, Optional, Set, Union

from connect_four.evaluation.victor.game import Board, Group, Square
from connect_four.evaluation.victor.solution import find_all_solutions, Solution
from connect_four.evaluation.victor.solution import combination
from connect_four.evaluation.victor.threat_hunter import Threat, ThreatCombination, ThreatCombinationType
from connect_four.evaluation.victor.threat_hunter import find_odd_threat, find_threat_combination


Evaluation = namedtuple("Evaluation", ["chosen_set", "odd_threat_guarantor"])


class EvaluationBuilder:
    def __init__(self):
        """
        Public Fields:
            chosen_set (Set<Solution>): a chosen set of Solutions the opponent can use that
                refutes all groups belonging to the current player.
            odd_threat_guarantor (Threat | ThreatCombination): A Threat or ThreatCombination for White.
        """
        self.chosen_set = None
        self.odd_threat_guarantor = None

    def set_chosen_set(self, chosen_set):
        self.chosen_set = chosen_set

    def set_odd_threat_guarantor(self, odd_threat_guarantor):
        self.odd_threat_guarantor = odd_threat_guarantor

    def build(self) -> Evaluation:
        if self.chosen_set is not None:
            return Evaluation(chosen_set=self.chosen_set, odd_threat_guarantor=self.odd_threat_guarantor)


def evaluate(board: Board) -> Optional[Evaluation]:
    """evaluate returns an Evaluation of the given Board instance.

    Args:
        board (Board): a Board instance.

    Returns:
        evaluation (Evaluation): an Evaluation of board.
    """
    player_groups = board.potential_groups(player=board.player)
    all_solutions = find_all_solutions(board=board)

    evaluation_builder = EvaluationBuilder()

    if board.player == 1:  # Current player is Black.
        # TODO consider if finding all possible odd group guarantors would be worth it.
        #  e.g. if an odd threat works even when a threat combination doesn't, we'd still use it.
        #  e.g. if a higher odd threat can be refuted but a lower odd threat cannot, we'd still use it.
        odd_threat_guarantor = find_odd_threat_guarantor(board=board)
        if odd_threat_guarantor is None:
            return None
        evaluation_builder.set_odd_threat_guarantor(odd_threat_guarantor=odd_threat_guarantor)
        player_groups = player_groups - problems_solved_by_odd_threat_guarantor(
            board=board,
            problems=player_groups,
            odd_threat_guarantor=odd_threat_guarantor,
        )
        all_solutions = all_solutions - unusable_solutions_with_guarantor(
            solutions=all_solutions,
            guarantor=odd_threat_guarantor,
        )

    node_graph = create_node_graph(solutions=all_solutions)
    # Only try to find a set that can solve all problems if every Problem has at least one Solution.
    if player_groups.issubset(node_graph.keys()):
        evaluation_builder.set_chosen_set(
            chosen_set=find_chosen_set(
                node_graph=node_graph,
                problems=player_groups,
                disallowed_solutions=set(),
                used_solutions=set(),
            )
        )
        return evaluation_builder.build()


def create_node_graph(solutions: Set[Solution]) -> Dict[Union[Group, Solution], Set[Solution]]:
    """create_node_graph accepts an iterable of Solutions and creates a graph connecting Problems and Solutions.
    Every Problem is connected to all Solutions that solve it.
    No Problem is connected to another Problem.
    Every Solution is connected to all Solutions that cannot be combined with it.

    Args:
        solutions (iterable<Solution>): an iterable of Solutions.

    Returns:
        node_graph (dict<Group|Solution, Set<Solution>>): a Dictionary of groups or
            Solutions to all Solutions they are connected to.
            Every Solution will at least be connected to itself.
    """
    node_graph = {}

    for solution in solutions:
        # Connect solution to all Problems it solves.
        for group in solution.groups:
            if group not in node_graph:
                node_graph[group] = set()
            node_graph[group].add(solution)

        # Connect all Solutions that cannot work with solution to solution.
        node_graph[solution] = set()
        for other in solutions:
            if not combination.allowed(s1=solution, s2=other):
                node_graph[solution].add(other)
    return node_graph


def find_chosen_set(
        node_graph: Dict[Union[Group, Solution], Set[Solution]],
        problems: Set[Group],
        disallowed_solutions: Set[Solution],
        used_solutions: Set[Solution]) -> Set[Solution]:
    """find_chosen_set finds a set of Solutions that solve all Problems.

    Args:
        node_graph (dict<Group|Solution, Set<Solution>>): a Dictionary of groups or
            Solutions to all Solutions they are connected to.
        problems (Set<Group>): a set of groups.
        disallowed_solutions (Set<Solution>): a set of available Solutions to solve problems.
        used_solutions (Set<Solution>): a set of Solutions that have already been used
            to solve Problems outside problems.

    Returns:
        chosen_set (Set<Solution>): a chosen set of Solutions that solves problems, if one exists.
            None if it doesn't.
    """
    # Base Case.
    if not problems:
        # If there are no problems, return the set of Solutions are currently using.
        return used_solutions.copy()

    # Recursive Case.
    most_difficult_node = node_with_least_number_of_neighbors(
        node_graph=node_graph, problems=problems, disallowed_solutions=disallowed_solutions)
    most_difficult_node_usable_solutions = node_graph[most_difficult_node].difference(disallowed_solutions)

    for solution in most_difficult_node_usable_solutions:
        # Choose.
        used_solutions.add(solution)
        # Recurse.
        chosen_set = find_chosen_set(
            node_graph=node_graph,
            problems=problems - solution.groups,
            disallowed_solutions=disallowed_solutions.union(node_graph[solution]),
            used_solutions=used_solutions,
        )
        # Unchoose.
        used_solutions.remove(solution)

        if chosen_set is not None:
            return chosen_set


def node_with_least_number_of_neighbors(
        node_graph: Dict[Union[Group, Solution], Set[Solution]],
        problems: Set[Group],
        disallowed_solutions: Set[Solution]):
    most_difficult_node = None
    num_neighbors_of_most_difficult = len(node_graph) + 1  # Set to an arbitrary high number.

    # Find the Problem in problems with the fewest neighbors in node_graph.
    # Only allowed_solutions are counted.
    for problem in problems:
        num_nodes = len(node_graph[problem].difference(disallowed_solutions))
        if num_nodes < num_neighbors_of_most_difficult:
            most_difficult_node = problem
            num_neighbors_of_most_difficult = num_nodes

    # If we didn't find a most_difficult_node, then that means there isn't a single Problem in both
    # problems and node_graph.
    if most_difficult_node is not None:
        return most_difficult_node

    raise ValueError("No problem in problems and node_graph")


def find_odd_threat_guarantor(board: Board) -> Union[Threat, ThreatCombination]:
    threat_combination = find_threat_combination(board=board)
    if threat_combination:
        return threat_combination
    return find_odd_threat(board=board)


def problems_solved_by_odd_threat_guarantor(
        board: Board, problems: Set[Group], odd_threat_guarantor: Union[Threat, ThreatCombination]) -> Set[Group]:
    if isinstance(odd_threat_guarantor, Threat):
        return problems_solved_by_odd_threat(board=board, problems=problems, odd_threat=odd_threat_guarantor)
    if isinstance(odd_threat_guarantor, ThreatCombination):
        if odd_threat_guarantor.threat_combination_type == ThreatCombinationType.EvenAboveOdd:
            return problems_solved_by_even_above_odd_threat_combination(
                board=board, problems=problems, threat_combination=odd_threat_guarantor)
        if odd_threat_guarantor.threat_combination_type == ThreatCombinationType.OddAboveDirectlyPlayableEven:
            return problems_solved_by_odd_above_directly_playable_even_threat_combination(
                board=board, problems=problems, threat_combination=odd_threat_guarantor)
        if odd_threat_guarantor.threat_combination_type == ThreatCombinationType.OddAboveNotDirectlyPlayableEven:
            return problems_solved_by_odd_above_not_directly_playable_even_threat_combination(
                board=board, problems=problems, threat_combination=odd_threat_guarantor)


def problems_solved_by_odd_threat(board: Board, problems: Set[Group], odd_threat: Threat) -> Set[Group]:
    directly_playable_square_in_odd_threat_col = board.playable_square(col=odd_threat.empty_square.col)
    problems_solved = set()
    # Add Groups containing any odd Square up to the Odd Threat that are not directly playable.
    for row in range(odd_threat.empty_square.row, directly_playable_square_in_odd_threat_col.row, 2):
        square = Square(row=row, col=odd_threat.empty_square.col)
        for problem in problems:
            if square in problem.squares:
                problems_solved.add(problem)
    # Add Groups containing any Squares above the odd Threat.
    for row in range(0, odd_threat.empty_square.row, 1):
        square = Square(row=row, col=odd_threat.empty_square.col)
        for problem in problems:
            if square in problem.squares:
                problems_solved.add(problem)
    return problems_solved


def problems_solved_by_even_above_odd_threat_combination(
        board: Board, problems: Set[Group], threat_combination: ThreatCombination) -> Set[Group]:
    if threat_combination.threat_combination_type != ThreatCombinationType.EvenAboveOdd:
        raise ValueError(
            "threat_combination.threat_combination_type =",
            threat_combination.threat_combination_type,
            "should be ThreatCombinationType.EvenAboveOdd",
        )

    problems_solved = set()

    # Add Groups containing any odd Square in the crossing column that are not directly playable.
    problems_solved.update(_no_odd_squares_in_crossing_column(
        board=board, problems=problems, threat_combination=threat_combination,
    ))

    # Add Groups containing a Square above the crossing square and a Square above the odd Square in the stacked column.
    problems_solved.update(_no_squares_above_crossing_and_above_odd(
        problems=problems, threat_combination=threat_combination,
    ))

    # Add Groups containing the Square above the crossing square and the upper Square in the stacked column.
    problems_solved.update(_groups_containing_square_above_crossing_and_upper_stacked(
        problems=problems, threat_combination=threat_combination,
    ))

    square_above_crossing = Square(
        row=threat_combination.shared_square.row - 1,
        col=threat_combination.shared_square.col,
    )
    directly_playable_square_in_stacked_col = board.playable_square(threat_combination.odd_square.col)
    # If the odd square in the stacked column is playable:
    if threat_combination.odd_square == directly_playable_square_in_stacked_col:
        # Add Groups containing any Square above square_above_crossing.
        for row in range(0, square_above_crossing.row, 1):
            square = Square(row=row, col=square_above_crossing.col)
            for problem in problems:
                if square in problem.squares:
                    problems_solved.add(problem)

    threat_combination_baseinverse_problems = _threat_combination_baseinverse(
        board=board, problems=problems, threat_combination=threat_combination,
    )
    problems_solved.update(threat_combination_baseinverse_problems)

    _threat_combination_baseinverse_applied = 0
    if threat_combination_baseinverse_problems:
        _threat_combination_baseinverse_applied = 1

    problems_solved.update(_vertical_groups_in_stacked_column(
        problems=problems,
        threat_combination=threat_combination,
        _threat_combination_baseinverse_applied=_threat_combination_baseinverse_applied,
    ))

    return problems_solved


def problems_solved_by_odd_above_not_directly_playable_even_threat_combination(
        board: Board, problems: Set[Group], threat_combination: ThreatCombination) -> Set[Group]:
    if threat_combination.threat_combination_type != ThreatCombinationType.OddAboveNotDirectlyPlayableEven:
        raise ValueError(
            "threat_combination.threat_combination_type =",
            threat_combination.threat_combination_type,
            "should be ThreatCombinationType.OddAboveNotDirectlyPlayableEven",
        )
    problems_solved = set()

    # Add Groups containing any odd Square in the crossing column that are not directly playable.
    problems_solved.update(_no_odd_squares_in_crossing_column(
        board=board, problems=problems, threat_combination=threat_combination,
    ))

    # Add Groups containing a Square above the crossing square and a Square above the odd Square in the stacked column.
    problems_solved.update(_no_squares_above_crossing_and_above_odd(
        problems=problems, threat_combination=threat_combination,
    ))

    # Add Groups containing the Square above the crossing square and the upper Square in the stacked column.
    # Note that the logic in the below line is not included in the original paper.
    problems_solved.update(_groups_containing_square_above_crossing_and_upper_stacked(
        problems=problems, threat_combination=threat_combination,
    ))

    threat_combination_baseinverse_problems = _threat_combination_baseinverse(
        board=board, problems=problems, threat_combination=threat_combination,
    )
    problems_solved.update(threat_combination_baseinverse_problems)

    _threat_combination_baseinverse_applied = 0
    if threat_combination_baseinverse_problems:
        _threat_combination_baseinverse_applied = 1

    problems_solved.update(_vertical_groups_in_stacked_column(
        problems=problems,
        threat_combination=threat_combination,
        _threat_combination_baseinverse_applied=_threat_combination_baseinverse_applied,
    ))

    return problems_solved


def problems_solved_by_odd_above_directly_playable_even_threat_combination(
        board: Board, problems: Set[Group], threat_combination: ThreatCombination) -> Set[Group]:
    if threat_combination.threat_combination_type != ThreatCombinationType.OddAboveDirectlyPlayableEven:
        raise ValueError(
            "threat_combination.threat_combination_type =",
            threat_combination.threat_combination_type,
            "should be ThreatCombinationType.OddAboveDirectlyPlayableEven",
        )
    problems_solved = set()

    # Add Groups containing any odd Square in the crossing column that are not directly playable.
    problems_solved.update(_no_odd_squares_in_crossing_column(
        board=board, problems=problems, threat_combination=threat_combination,
    ))

    # Add Groups containing a Square above the crossing square and a Square above the odd Square in the stacked column.
    problems_solved.update(_no_squares_above_crossing_and_above_odd(
        problems=problems, threat_combination=threat_combination,
    ))

    # Add Groups containing the Square above the crossing square and the upper Square in the stacked column.
    # Note that the logic in the below line is not included in the original paper.
    problems_solved.update(_groups_containing_square_above_crossing_and_upper_stacked(
        problems=problems, threat_combination=threat_combination,
    ))

    # Note that the logic in the below line is not included in the original paper.
    problems_solved.update(_vertical_groups_in_stacked_column(
        problems=problems,
        threat_combination=threat_combination,
        _threat_combination_baseinverse_applied=0,
    ))

    return problems_solved


def _no_odd_squares_in_crossing_column(
        board: Board, problems: Set[Group], threat_combination: ThreatCombination) -> Set[Group]:
    directly_playable_square_in_shared_col = board.playable_square(col=threat_combination.shared_square.col)
    problems_solved = set()

    # Add Groups containing any odd Square in the crossing column that are not directly playable.
    for row in range(threat_combination.shared_square.row, directly_playable_square_in_shared_col.row, 2):
        square = Square(row=row, col=threat_combination.shared_square.col)
        for problem in problems:
            if square in problem.squares:
                problems_solved.add(problem)

    return problems_solved


def _no_squares_above_crossing_and_above_odd(
        problems: Set[Group], threat_combination: ThreatCombination) -> Set[Group]:
    problems_solved = set()
    # Add Groups containing a Square above the crossing square and a Square above the odd Square in the stacked column.
    for row_in_crossing_col in range(0, threat_combination.shared_square.row, 1):
        square_above_crossing = Square(row=row_in_crossing_col, col=threat_combination.shared_square.col)
        for row_in_stacked_col in range(0, threat_combination.odd_square.row, 1):
            square_above_stacked = Square(row=row_in_stacked_col, col=threat_combination.odd_square.col)
            for problem in problems:
                if square_above_crossing in problem.squares and square_above_stacked in problem.squares:
                    problems_solved.add(problem)
    return problems_solved


def _groups_containing_square_above_crossing_and_upper_stacked(
        problems: Set[Group], threat_combination: ThreatCombination) -> Set[Group]:
    problems_solved = set()

    square_above_crossing = Square(
        row=threat_combination.shared_square.row - 1,
        col=threat_combination.shared_square.col,
    )
    # Add Groups containing the Square above the crossing square and the upper Square in the stacked column.
    for problem in problems:
        if (square_above_crossing in problem.squares and
                threat_combination.upper_square_in_stacked_column() in problem.squares):
            problems_solved.add(problem)

    return problems_solved


def _threat_combination_baseinverse(
        board: Board, problems: Set[Group], threat_combination: ThreatCombination) -> Set[Group]:
    directly_playable_square_in_shared_col = board.playable_square(col=threat_combination.shared_square.col)
    directly_playable_square_in_stacked_col = board.playable_square(col=threat_combination.odd_square.col)
    problems_solved = set()

    # If the first empty square in the crossing column is odd and
    # the odd square in the stacked column is not directly playable:
    if (directly_playable_square_in_shared_col.row % 2 == 1 and
            threat_combination.odd_square != directly_playable_square_in_stacked_col):
        # Add Groups containing the lowest squares of both columns.
        for problem in problems:
            if (directly_playable_square_in_shared_col in problem.squares and
                    directly_playable_square_in_stacked_col in problem.squares):
                problems_solved.add(problem)

    return problems_solved


def _vertical_groups_in_stacked_column(
        problems: Set[Group],
        threat_combination: ThreatCombination,
        _threat_combination_baseinverse_applied: int) -> Set[Group]:
    problems_solved = set()
    # In the stacked column, add Groups containing two Squares on top of each other
    # up to and including the odd square in that column.
    # If a baseinverse is applied for the ThreatCombination, this observation starts one square higher.
    for upper_row in range(0, threat_combination.odd_square.row - _threat_combination_baseinverse_applied, 1):
        upper = Square(row=upper_row, col=threat_combination.odd_square.col)
        lower = Square(row=upper_row + 1, col=threat_combination.odd_square.col)
        for problem in problems:
            if upper in problem.squares and lower in problem.squares:
                problems_solved.add(problem)

    return problems_solved


def unusable_solutions_with_guarantor(
        solutions: Set[Solution], guarantor: Union[Threat, ThreatCombination]) -> Set[Solution]:
    unusable_columns = []
    if isinstance(guarantor, Threat):
        unusable_columns.append(guarantor.empty_square.col)
    elif isinstance(guarantor, ThreatCombination):
        unusable_columns.append(guarantor.shared_square.col)
        unusable_columns.append(guarantor.even_square.col)

    unusable_solutions = set()
    for solution in solutions:
        for square in solution.squares:
            if square.col in unusable_columns:
                unusable_solutions.add(solution)
    return unusable_solutions
