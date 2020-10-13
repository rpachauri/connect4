# Gotta import gym!
import gym
import connect_four

from connect_four.agents.minimax_agent import Minimax


# Make the environment, replace this string with any
# from the docs. (Some environments have dependencies)
env = gym.make('connect_four-v0')

# Initialize the agents
agent1 = Minimax(max_depth=6)
agent2 = Minimax(max_depth=4)


# Reset the environment to default beginning
# Default observation variable
obs = env.reset()
env.render()

done = False

while not done:
  # Let the agent whose turn it is select an action.
  action = -1
  if env.player_turn == 0:
    action = agent1.action(env)
  else:
    action = agent2.action(env)

  print("Player", (env.player_turn + 1), "is placing a token in column:", action)
  _, reward, done, info = env.step(action)

  # Render the env
  env.render()

  print("Received reward:", reward)

  if done:
    break