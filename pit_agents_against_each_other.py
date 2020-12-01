# Gotta import gym!
import gym

from connect_four.agents import FlatMonteCarlo
from connect_four.agents import FlatUCB
from connect_four.agents import MCPNS
from connect_four.agents import Minimax
from connect_four.agents import RandomAgent
from connect_four.envs import ConnectFourEnv

# Make the environment, replace this string with any
# from the docs. (Some environments have dependencies)
env = gym.make('connect_four-v0')

agents_record = [0, 0, 0]

for i in range(10):
    # Initialize the agents
    agent1 = FlatMonteCarlo(num_rollouts=1000)  # Minimax(max_depth=3)
    agent2 = FlatUCB(num_rollouts=1000)  # RandomAgent()  # MCPNS(num_rollouts=2000)

    # Reset the environment to default beginning
    # Default observation variable
    obs = env.reset()

    done = False
    last_action = None

    while not done:
        # Let the agent whose turn it is select an action.
        if env.player_turn == 0:
            last_action = agent1.action(env, last_action)
        else:
            last_action = agent2.action(env, last_action)

        _, reward, done, info = env.step(last_action)

        if done:
            if reward == ConnectFourEnv.CONNECTED_FOUR:
                agents_record[env.player_turn] += 1
            elif reward == ConnectFourEnv.INVALID_MOVE:
                agents_record[1 - env.player_turn] += 1
            else:  # reward == ConnectFourEnv.DRAW
                agents_record[2] += 1

    print("Finished game", i)

print("Number of wins for agent 1:", agents_record[0])
print("Number of wins for agent 2:", agents_record[1])
print("Number of draws for both agents:", agents_record[2])