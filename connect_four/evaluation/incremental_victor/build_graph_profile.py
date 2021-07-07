import cProfile
from typing import Set, Dict

import gym

from connect_four.evaluation.board import Board
from connect_four.evaluation.incremental_victor.solution import victor_solution
from connect_four.evaluation.incremental_victor.solution.solution import Solution
from connect_four.evaluation.incremental_victor.solution.victor_solution import VictorSolution
from connect_four.evaluation.victor.rules import find_all_claimevens, find_all_baseinverses, find_all_verticals, \
    find_all_afterevens, find_all_lowinverses, find_all_highinverses_using_highinverse_columns, find_all_baseclaims, \
    find_all_befores, find_all_specialbefores
from connect_four.problem.problem import Problem


def build_graph_n(board: Board, n: int):
    for _ in range(n):
        build_graph(board=board)


def build_graph(board: Board) -> (Dict[Problem, Set[Solution]], Dict[Solution, Set[Problem]]):
    solutions = find_all_solutions(board=board)
    white_problems = board.potential_groups(player=0)

    problem_to_solutions: Dict[Problem, Set[Solution]] = {}
    solution_to_problems: Dict[Solution, Set[Problem]] = {}

    for problem in white_problems:
        problem_to_solutions[problem] = set()

    for solution in solutions:
        solved_problems = set()
        for problem in white_problems:
            if solution.solves(problem=problem):
                solved_problems.add(problem)
        if solution.is_useful(problems=solved_problems):
            solution_to_problems[solution] = solved_problems
            for problem in solved_problems:
                problem_to_solutions[problem].add(solution)

    return problem_to_solutions, solution_to_problems


def find_all_solutions(board: Board) -> Set[VictorSolution]:
    """Finds all Solutions for the current board.

    Returns:
        solutions (Set[VictorSolution]): the set of all Solutions for either player in the current board.
    """
    # white_groups = board.potential_groups(0)
    black_groups = board.potential_groups(1)

    # Find all applications of all rules.
    claimevens = find_all_claimevens(board=board)
    baseinverses = find_all_baseinverses(board=board)
    verticals = find_all_verticals(board=board)
    # white_afterevens = find_all_afterevens(board=board, opponent_groups=white_groups)
    black_afterevens = find_all_afterevens(board=board, opponent_groups=black_groups)
    lowinverses = find_all_lowinverses(verticals=verticals)
    highinverses = find_all_highinverses_using_highinverse_columns(board=board)
    baseclaims = find_all_baseclaims(board=board)
    # white_befores = find_all_befores(board=board, opponent_groups=white_groups)
    # white_specialbefores = find_all_specialbefores(board=board, befores=white_befores)
    black_befores = find_all_befores(board=board, opponent_groups=black_groups)
    black_specialbefores = find_all_specialbefores(board=board, befores=black_befores)
    # Find all win conditions for White.
    # white_odd_threats = find_all_oddthreats(board=board)

    # Convert the rule instances into Solutions.
    solutions = set()
    for claimeven in claimevens:
        solutions.add(victor_solution.from_claimeven(claimeven=claimeven))
    for baseinverse in baseinverses:
        solutions.add(victor_solution.from_baseinverse(baseinverse=baseinverse))
    for vertical in verticals:
        solutions.add(victor_solution.from_vertical(vertical=vertical))
    # for aftereven in white_afterevens:
    #     solutions.add(victor_solution.from_aftereven(aftereven=aftereven))
    for aftereven in black_afterevens:
        solutions.add(victor_solution.from_aftereven(aftereven=aftereven))
    for lowinverse in lowinverses:
        solutions.add(victor_solution.from_lowinverse(lowinverse=lowinverse))
    for highinverse in highinverses:
        solutions.add(victor_solution.from_highinverse(highinverse=highinverse))
    for baseclaim in baseclaims:
        solutions.add(victor_solution.from_baseclaim(baseclaim=baseclaim))
    # for before in white_befores:
    #     solutions.add(victor_solution.from_before(before=before))
    for before in black_befores:
        solutions.add(victor_solution.from_before(before=before))
    # for specialbefore in white_specialbefores:
    #     solutions.add(victor_solution.from_specialbefore(specialbefore=specialbefore))
    for specialbefore in black_specialbefores:
        solutions.add(victor_solution.from_specialbefore(specialbefore=specialbefore))
    # for odd_threat in white_odd_threats:
    #     solutions.add(solution2.from_odd_threat(odd_threat=odd_threat))

    return solutions


env = gym.make('connect_four-v0')
env.reset()

empty_board = Board(env_variables=env.env_variables)

cProfile.run(
    'build_graph_n(board=empty_board, n=10)',
    sort="cumtime",
)
