# Gotta import gym!
import gym
import connect_four

from connect_four.agents.minimax_agent import Minimax


# Make the environment, replace this string with any
# from the docs. (Some environments have dependencies)
env = gym.make('connect_four-v0')

# Initialize the agents
agent = Minimax()

# Reset the environment to default beginning
# Default observation variable
obs = env.reset()
env.render()

done = False

while not done:
  action = agent.action(env)
  print("Player", env.player_turn, "is placing a token in column:", action)
  _, reward, done, info = env.step(action)

  # Render the env
  env.render()

  print("Received reward:", reward)

  if done:
    break