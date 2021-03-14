# Required in order to type hint a method with the type of the enclosing class.
# See https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class.
from __future__ import annotations

from connect_four.agents.agent import Agent

from connect_four.evaluation import Evaluator
from connect_four.evaluation.evaluator import ProofStatus


class PNSNode:
    def __init__(self):
        self.status = ProofStatus.Unknown
        self.proof = 0
        self.disproof = 0
        self.children = {}

    def __eq__(self, other):
        if isinstance(other, PNSNode):
            return (self.status == other.status and
                    self.proof == other.proof and
                    self.disproof == other.disproof and
                    self.children == other.children)

    def update_tree(self, evaluator: Evaluator):
        pass

    def expand(self, evaluator: Evaluator):
        pass

    def set_proof_and_disproof_numbers(self):
        pass

    def select_most_proving_child(self) -> (int, PNSNode):
        pass


class PNS(Agent):
    def action(self, env, last_action=None):
        pass
