import gym
import numpy as np

import cProfile

from connect_four.evaluation.victor.board import Board
from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.evaluation.victor.evaluator import evaluator

env = gym.make('connect_four-v0')
ConnectFourEnv.M = 6
ConnectFourEnv.N = 7

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
board = Board(env.env_variables)


def evaluate_move_to_provable_state_and_evaluate():
    evaluator.evaluate(board=board)
    board.state[0][5][0] = 1  # White plays a1
    evaluator.evaluate(board=board)
    board.state[1][5][1] = 1  # Black plays b1
    evaluator.evaluate(board=board)
    board.state[0][4][2] = 1  # White plays b2
    evaluator.evaluate(board=board)
    board.state[1][2][3] = 1  # Black plays d4
    evaluator.evaluate(board=board)
    board.state[0][3][1] = 1  # White plays b3
    evaluator.evaluate(board=board)
    board.state[1][3][4] = 1  # Black plays e3
    evaluator.evaluate(board=board)
    board.state[0][2][4] = 1  # White plays e4
    evaluator.evaluate(board=board)


cProfile.run('evaluate_move_to_provable_state_and_evaluate()', sort="cumtime")
