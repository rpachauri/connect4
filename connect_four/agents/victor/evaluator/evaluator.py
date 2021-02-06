"""
Note that in this module, we use the term "Group" and "Problem" interchangeably.
"""
from collections import namedtuple

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.solution import find_all_solutions, combination


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


def evaluate(board: Board) -> Evaluation:
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
        raise NotImplementedError()
    pass


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
