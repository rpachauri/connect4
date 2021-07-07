import cProfile

import gym

import numpy as np

from connect_four.evaluation.incremental_victor.graph.graph_manager import GraphManager
from connect_four.evaluation.victor.solution import VictorSolutionManager
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


def evaluate_move_to_provable_state_and_evaluate():
    gm = GraphManager(player=0, problem_manager=cfgm, solution_manager=vsm)
    gm.evaluate()
    gm.move(row=5, col=0)  # White plays a1
    gm.evaluate()
    gm.move(row=5, col=1)  # Black plays b1
    gm.evaluate()
    gm.move(row=4, col=1)  # White plays b2
    gm.evaluate()
    gm.move(row=2, col=3)  # Black plays d4
    gm.evaluate()
    gm.move(row=3, col=1)  # White plays b3
    gm.evaluate()
    gm.move(row=3, col=4)  # Black plays e3
    gm.evaluate()
    gm.move(row=2, col=4)  # White plays e4
    gm.evaluate()


cProfile.run(
    'evaluate_move_to_provable_state_and_evaluate()',
    sort="cumtime",
)
