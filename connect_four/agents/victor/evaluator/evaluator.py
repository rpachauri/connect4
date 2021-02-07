"""
Note that in this module, we use the term "Group" and "Problem" interchangeably.
"""
from collections import namedtuple
from typing import Optional
from typing import Set

from connect_four.agents.victor.game import Board, Group, Square
from connect_four.agents.victor.solution import find_all_solutions, combination, Solution
from connect_four.agents.victor.threat_hunter import Threat
from connect_four.agents.victor.threat_hunter import find_odd_threat


Evaluation = namedtuple("Evaluation", ["chosen_set", "odd_threat_guarantor"])


class EvaluationBuilder:
    def __init__(self):
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
    """evaluate finds a set of Solutions the opponent can use to
    refute all groups belonging to the current player, if such a set of Solutions exists.

    Args:
        board (Board): a Board instance.

    Returns:
        chosen_set (Set<Solution>): a chosen set of Solutions the opponent can use that
            refutes all groups belonging to the current player, if one exists.
            None if no such set of Solutions exist.
    """
    player_groups = board.potential_groups(player=board.player)
    all_solutions = find_all_solutions(board=board)

    evaluation_builder = EvaluationBuilder()

    if board.player == 0:  # Current player is White.
        node_graph = create_node_graph(solutions=all_solutions)
        # Only try to find a set that can solve all problems if every Problem has at least one Solution.
        if player_groups.issubset(node_graph.keys()):
            evaluation_builder.set_chosen_set(
                chosen_set=find_chosen_set(
                    node_graph=node_graph,
                    problems=player_groups,
                    allowed_solutions=all_solutions,
                    used_solutions=set(),
                )
            )
            return evaluation_builder.build()
    else:
        odd_threat_guarantor = find_odd_threat_guarantor(board=board)
        if odd_threat_guarantor is None:
            return None
        evaluation_builder.set_odd_threat_guarantor(odd_threat_guarantor=odd_threat_guarantor)
        player_groups = player_groups - problems_solved_by_guarantor(
            board=board,
            problems=player_groups,
            guarantor=odd_threat_guarantor,
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
                    allowed_solutions=all_solutions,
                    used_solutions=set(),
                )
            )
            return evaluation_builder.build()


def create_node_graph(solutions):
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


def find_chosen_set(node_graph, problems, allowed_solutions, used_solutions):
    """find_chosen_set finds a set of Solutions that solve all Problems.

    Args:
        node_graph (dict<Group|Solution, Set<Solution>>): a Dictionary of groups or
            Solutions to all Solutions they are connected to.
        problems (Set<Group>): a set of groups.
        allowed_solutions (Set<Solution>): a set of available Solutions to solve problems.
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
        node_graph=node_graph, problems=problems, allowed_solutions=allowed_solutions)
    most_difficult_node_usable_solutions = node_graph[most_difficult_node].intersection(allowed_solutions)

    for solution in most_difficult_node_usable_solutions:
        # Choose.
        used_solutions.add(solution)
        # Recurse.
        chosen_set = find_chosen_set(
            node_graph=node_graph,
            problems=problems - solution.groups,
            allowed_solutions=allowed_solutions - node_graph[solution],
            used_solutions=used_solutions,
        )
        # Unchoose.
        used_solutions.remove(solution)

        if chosen_set is not None:
            return chosen_set


def node_with_least_number_of_neighbors(node_graph, problems, allowed_solutions):
    most_difficult_node = None
    num_neighbors_of_most_difficult = len(allowed_solutions) + 1  # Set to an arbitrary high number.

    # Find the Problem in problems with the fewest neighbors in node_graph.
    # Only allowed_solutions are counted.
    for problem in problems:
        num_nodes = len(node_graph[problem].intersection(allowed_solutions))
        if num_nodes < num_neighbors_of_most_difficult:
            most_difficult_node = problem
            num_neighbors_of_most_difficult = num_nodes

    # If we didn't find a most_difficult_node, then that means there isn't a single Problem in both
    # problems and node_graph.
    if most_difficult_node is not None:
        return most_difficult_node

    raise ValueError("No problem in problems and node_graph")


def find_odd_threat_guarantor(board: Board):
    return find_odd_threat(board=board)


def problems_solved_by_guarantor(board: Board, problems: Set[Group], guarantor: Threat) -> Set[Group]:
    directly_playable_square_in_odd_threat_col = board.playable_square(col=guarantor.empty_square.col)
    problems_solved = set()
    if isinstance(guarantor, Threat):
        for row in range(guarantor.empty_square.row, directly_playable_square_in_odd_threat_col.row, 2):
            square = Square(row=row, col=guarantor.empty_square.col)
            for problem in problems:
                if square in problem.squares:
                    problems_solved.add(problem)
        for row in range(guarantor.empty_square.row, 0, -1):
            square = Square(row=row, col=guarantor.empty_square.col)
            for problem in problems:
                if square in problem.squares:
                    problems_solved.add(problem)
        return problems_solved


def unusable_solutions_with_guarantor(solutions: Set[Solution], guarantor: Threat) -> Set[Solution]:
    unusable_columns = []
    if isinstance(guarantor, Threat):
        unusable_columns.append(guarantor.empty_square)

    unusable_solutions = set()
    for solution in solutions:
        for square in solution.squares:
            if square.col in unusable_columns:
                unusable_solutions.add(solution)
    return unusable_solutions
