import gym

import time

from connect_four.agents import DFPN
from connect_four.agents import difficult_connect_four_positions
from connect_four.evaluation.victor.victor_evaluator import Victor
from connect_four.hashing import ConnectFourHasher
from connect_four.transposition.sqlite_transposition_table import SQLiteTranspositionTable

env = gym.make('connect_four-v0')

env.reset(env_variables=difficult_connect_four_positions.diagram_13_14)

evaluator = Victor(model=env)
hasher = ConnectFourHasher(env=env)
tt = SQLiteTranspositionTable(database_file="connect_four.db")
agent = DFPN(evaluator, hasher, tt)

start = time.time()
evaluation = agent.depth_first_proof_number_search(env=env)
end = time.time()
print(evaluation)
print("time to run = ", end - start)
tt.close()
