# Gotta import gym!
import gym
import connect_four

from connect_four.agents import Minimax


# Make the environment, replace this string with any
# from the docs. (Some environments have dependencies)
env = gym.make('connect_four-v0')

# Initialize the agents
agent1 = Minimax(max_depth=4)
agent2 = Minimax(max_depth=3)


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