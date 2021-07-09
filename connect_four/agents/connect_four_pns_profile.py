import gym
import numpy as np

import cProfile

from connect_four.agents import DFPN, PNS
from connect_four.evaluation.victor.victor_evaluator import Victor
from connect_four.hashing import ConnectFourHasher
from connect_four.transposition.dbm_transposition_table import DBMTranspositionTable
from connect_four.transposition.simple_transposition_table import SimpleTranspositionTable

diagram_11_1 = np.array([
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
diagram_13_6 = np.array([
    [
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 1, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 1, 0, 0, 0, ],
        [0, 1, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 1, 0, 0, 0, ],
    ],
    [
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 1, 0, 0, 0, ],
        [0, 0, 0, 0, 0, 0, 0, ],
        [0, 0, 0, 1, 0, 0, 0, ],
        [0, 1, 0, 0, 0, 0, 0, ],
    ],
])


env = gym.make('connect_four-v0')

env.reset()
# This state is based on Diagram 11.1.
env.state = diagram_13_6
env.player_turn = 1

# The above state of Connect Four is a win for White, which means it is proven for OR.

evaluator = Victor(model=env)
hasher = ConnectFourHasher(env=env)
tt = DBMTranspositionTable(phi_file="connect_four_phi", delta_file="connect_four_delta")
agent = DFPN(evaluator, hasher, tt)
# agent = PNS(evaluator=evaluator)

# The given node should be proven.
cProfile.run(
    'print(agent.depth_first_proof_number_search(env=env))',
    sort="cumtime",
)

# cProfile.run(
#     'agent.proof_number_search()',
#     sort="cumtime",
# )
