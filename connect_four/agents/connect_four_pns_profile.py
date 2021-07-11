import gym
import numpy as np

import cProfile

from connect_four.agents import DFPN, PNS, difficult_connect_four_positions
from connect_four.evaluation.victor.victor_evaluator import Victor
from connect_four.hashing import ConnectFourHasher
from connect_four.transposition.dbm_transposition_table import DBMTranspositionTable
from connect_four.transposition.simple_transposition_table import SimpleTranspositionTable

env = gym.make('connect_four-v0')

env.reset(env_variables=difficult_connect_four_positions.diagram_11_1)

evaluator = Victor(model=env)
hasher = ConnectFourHasher(env=env)
# tt = DBMTranspositionTable(phi_file="connect_four_phi", delta_file="connect_four_delta")
tt = SimpleTranspositionTable()
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
