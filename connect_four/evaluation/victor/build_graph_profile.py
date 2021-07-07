import cProfile

import gym

from connect_four.evaluation.board import Board
from connect_four.evaluation.victor.solution import find_all_solutions


def build_graph_n(board: Board, n: int):
    for _ in range(n):
        find_all_solutions(board=board)


env = gym.make('connect_four-v0')
env.reset()

empty_board = Board(env_variables=env.env_variables)

cProfile.run(
    'build_graph_n(board=empty_board, n=10)',
    sort="cumtime",
)
