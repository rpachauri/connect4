import gym
import numpy as np

import cProfile

from connect_four.evaluation.victor.board import Board
from connect_four.envs.connect_four_env import ConnectFourEnv

env = gym.make('connect_four-v0')
ConnectFourEnv.M = 6
ConnectFourEnv.N = 7

# The empty 6x7 board has no solution set for Black because White is guaranteed to win.
env.state = np.array([
    [
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
    ],
    [
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
    ],
])
board = Board(env.env_variables)

cProfile.run('evaluator.evaluate(board=board)', sort="cumtime")
