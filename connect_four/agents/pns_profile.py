import gym
import numpy as np

import cProfile

from connect_four.agents import DFPN, PNS
from connect_four.evaluation import NodeType
from connect_four.evaluation.simple_evaluator import SimpleEvaluator
from connect_four.hashing import TicTacToeHasher
from connect_four.transposition.simple_transposition_table import SimpleTranspositionTable

env = gym.make('tic_tac_toe-v0')

env.reset()

# The initial state of Tic-Tac-Toe is a known draw, which means it is disproven for OR.
evaluator = SimpleEvaluator(model=env)
hasher = TicTacToeHasher(env=env)
tt = SimpleTranspositionTable()
agent = DFPN(evaluator, hasher, tt)
# agent = PNS(evaluator=evaluator)

# The given node should be easily proven even with phi/delta thresholds of 1.
cProfile.run(
    'agent.multiple_iterative_deepening(env=env, phi_threshold=DFPN.INF, delta_threshold=DFPN.INF)',
    sort="cumtime",
)

# cProfile.run(
#     'agent.action(env=env)',
#     sort="cumtime",
# )
