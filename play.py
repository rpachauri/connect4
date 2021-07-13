# Gotta import gym!
import gym

from connect_four.agents import FlatMonteCarlo, DFPN
from connect_four.agents import FlatUCB
from connect_four.agents import MCPNS
from connect_four.agents import MCTS
from connect_four.agents import Minimax
from connect_four.agents import RandomAgent
from connect_four.agents import PNS
from connect_four.agents.human import Human
from connect_four.evaluation import Victor

from connect_four.evaluation.evaluator import NodeType
from connect_four.evaluation.simple_evaluator import SimpleEvaluator

# Make the environment, replace this string with any
# from the docs. (Some environments have dependencies)
from connect_four.hashing import ConnectFourHasher
from connect_four.transposition.sqlite_transposition_table import SQLiteTranspositionTable

env = gym.make('connect_four-v0')
# env = gym.make('tic_tac_toe-v0')

# Initialize the agents
evaluator = Victor(model=env)
hasher = ConnectFourHasher(env=env)
tt = SQLiteTranspositionTable(database_file="connect_four.db")
agent1 = DFPN(evaluator, hasher, tt)
# agent1 = MCPNS(num_rollouts=30)  # Minimax(max_depth=9)
# agent2 = MCPNS(num_rollouts=30)
# evaluator = SimpleEvaluator(model=env)
# agent2 = PNS(evaluator=evaluator)
agent2 = Human()

# Reset the environment to default beginning
# Default observation variable
obs = env.reset()
env.render()

done = False
last_action = None

while not done:
    # Let the agent whose turn it is select an action.
    if env.player_turn == 0:
        last_action = agent1.action(env, last_action)
    else:
        last_action = agent2.action(env, last_action)

    print("Player", (env.player_turn + 1), "is placing a token in column:", last_action)
    _, reward, done, info = env.step(last_action)

    # Render the env
    env.render()

    print("Received reward:", reward)

    if done:
        break
