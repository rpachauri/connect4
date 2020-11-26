import random

from connect_four.agents.agent import Agent


class RandomAgent(Agent):

    def __init__(self):
        pass

    def action(self, env, last_action):
        return random.randint(0, env.action_space - 1)
