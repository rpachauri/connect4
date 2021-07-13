from connect_four.agents.agent import Agent


class Human(Agent):
    def action(self, env, last_action=None):
        return int(input("requesting action: "))
