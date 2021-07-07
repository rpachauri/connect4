import cProfile

import gym

import numpy as np

from connect_four.evaluation.incremental_victor.graph.graph_manager import GraphManager
from connect_four.evaluation.incremental_victor.solution.victor_solution_manager import VictorSolutionManager
from connect_four.problem import ConnectFourGroupManager

env = gym.make('connect_four-v0')
env.state = np.array([
    [
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 1, 1, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 1, 1, 0, 0, 0, ],
    ],
    [
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 1, 1, 1, 0, 0, ],
        [0, 0, 0, 0, 1, 0, 0, ],
    ],
])

# noinspection SpellCheckingInspection
cfgm = ConnectFourGroupManager(env_variables=env.env_variables)
vsm = VictorSolutionManager(env_variables=env.env_variables)

player, row, col = 0, 5, 0

gm = GraphManager(player=player, problem_manager=cfgm, solution_manager=vsm)

_, removed_problems = cfgm.move(player=player, row=row, col=col)
for problem in removed_problems:
    gm._remove_problem(problem)

removed_solutions, added_solutions = vsm.move(player=player, row=row, col=col)
print("len(removed_solutions) = ", len(removed_solutions))
print("len(added_solutions) = ", len(added_solutions))
# print("number of useful solutions =", len(self.solution_to_solutions))
for solution in removed_solutions:
    gm._remove_solution(solution)
print("number of solutions that remained =", len(gm.solution_to_solutions))


def add_solutions():
    for solution in added_solutions:
        gm._add_solution(solution)

    print("number of solutions after adding =", len(gm.solution_to_solutions))


cProfile.run(
    'add_solutions()',
    sort="cumtime",
)
