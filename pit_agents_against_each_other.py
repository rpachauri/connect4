# Gotta import gym!
import gym

from connect_four.agents import FlatMonteCarlo, DFPN
from connect_four.agents import FlatUCB
from connect_four.agents import MCPNS
from connect_four.agents import MCTS
from connect_four.agents import Minimax
from connect_four.agents import RandomAgent
from connect_four.agents import UCT
from connect_four.envs import TwoPlayerGameEnv
from connect_four.envs import ConnectFourEnv

# Make the environment, replace this string with any
# from the docs. (Some environments have dependencies)
from connect_four.evaluation import Victor
from connect_four.hashing import ConnectFourHasher
from connect_four.transposition.sqlite_transposition_table import SQLiteTranspositionTable

env = gym.make('connect_four-v0')

agents_record = [0, 0, 0]

for i in range(10):
    # Reset the environment to default beginning
    # Default observation variable
    obs = env.reset()
    done = False
    last_action = None

    # Initialize the agents
    evaluator = Victor(model=env)
    hasher = ConnectFourHasher(env=env)
    tt = SQLiteTranspositionTable(database_file="connect_four.db")
    agent1 = DFPN(evaluator, hasher, tt)
    # agent2 = FlatUCB(num_rollouts=1000)
    # agent2 = UCT(num_rollouts=1000)
    agent2 = Minimax(max_depth=5)

    while not done:
        # Let the agent whose turn it is select an action.
        if env.player_turn == 0:
            last_action = agent1.action(env, last_action)
        else:
            last_action = agent2.action(env, last_action)

        _, reward, done, info = env.step(last_action)

        if done:
            if reward == TwoPlayerGameEnv.CONNECTED:
                agents_record[env.player_turn] += 1
            elif reward == TwoPlayerGameEnv.INVALID_MOVE:
                agents_record[1 - env.player_turn] += 1
            else:  # reward == TwoPlayerGameEnv.DRAW
                agents_record[2] += 1

    print("Record after board", i, "-", agents_record)

print("Number of wins for agent 1:", agents_record[0])
print("Number of wins for agent 2:", agents_record[1])
print("Number of draws for both agents:", agents_record[2])
