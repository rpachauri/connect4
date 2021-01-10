"""
Note that in this module, we use the term "Threat" and "Problem" interchangeably.
"""
from connect_four.agents.victor.game import Board
from connect_four.agents.victor.evaluator import combination


def evaluate(board: Board):
    """evaluate finds a set of Solutions the opponent can use to
    refute all Threats belonging to the current player, if such a set of Solutions exists.

    Args:
        board (Board): a Board instance.

    Returns:
        chosen_set (Set<Solution>): a chosen set of Solutions the opponent can use that
            refutes all Threats belonging to the current player, if one exists.
            None if no such set of Solutions exist.
    """
    pass


def create_node_graph(solutions):
    """create_node_graph accepts an iterable of Solutions and creates a graph connecting Problems and Solutions.
    Every Problem is connected to all Solutions that solve it.
    No Problem is connected to another Problem.
    Every Solution is connected to all Solutions that cannot be combined with it.

    Args:
        solutions (iterable<Solution>): an iterable of Solutions.

    Returns:
        node_graph (dict<Threat|Solution, Set<Solution>>): a Dictionary of Threats or
            Solutions to all Solutions they are connected to.
    """
    node_graph = {}

    for solution in solutions:
        # Connect solution to all Problems it solves.
        for threat in solution.threats:
            if threat not in node_graph:
                node_graph[threat] = set()
            node_graph[threat].add(solution)

        # Connect all Solutions that cannot work with solution to solution.
        node_graph[solution] = set()
        for other in solutions:
            if other != solution and not combination.allowed(s1=solution, s2=other):
                node_graph[solution].add(other)
    return node_graph


def find_chosen_set(node_graph, problems, allowed_solutions, used_solutions):
    """find_chosen_set finds a set of Solutions that solve all Problems.

    Args:
        node_graph (dict<Threat|Solution, Set<Solution>>): a Dictionary of Threats or
            Solutions to all Solutions they are connected to.
        problems (Set<Threat>): a set of Threats.
        allowed_solutions (Set<Solution>): a set of available Solutions to solve problems.
        used_solutions (Set<Solution>): a set of Solutions that have already been used
            to solve Problems outside problems.

    Returns:
        chosen_set (Set<Solution>): a chosen set of Solutions that solves problems, if one exists.
            None if it doesn't.
    """
    pass
