import gym
import numpy as np

import cProfile

from connect_four.agents import DFPN, PNS
from connect_four.evaluation.incremental_victor_evaluator import IncrementalVictor
from connect_four.evaluation.victor_evaluator import Victor
from connect_four.hashing import ConnectFourHasher
from connect_four.transposition.simple_transposition_table import SimpleTranspositionTable

env = gym.make('connect_four-v0')

env.reset()
# This state is based on Diagram 11.1.
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

# The above state of Connect Four is a win for White, which means it is proven for OR.

evaluator = IncrementalVictor(model=env)
hasher = ConnectFourHasher(env=env)
tt = SimpleTranspositionTable()
agent = DFPN(evaluator, hasher, tt)
# agent = PNS(evaluator=evaluator)

# The given node should be proven.
cProfile.run(
    'agent.multiple_iterative_deepening(env=env, phi_threshold=DFPN.INF, delta_threshold=DFPN.INF)',
    sort="cumtime",
)

# cProfile.run(
#     'agent.proof_number_search()',
#     sort="cumtime",
# )
