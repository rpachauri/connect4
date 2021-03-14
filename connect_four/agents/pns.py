from connect_four.agents.agent import Agent
from connect_four.evaluation.evaluator import ProofStatus


class PNSNode:
    def __init__(self):
        self.status = ProofStatus.Unknown
        self.proof = 0
        self.disproof = 0
        self.children = {}


class PNS(Agent):
    def action(self, env, last_action=None):
        pass
