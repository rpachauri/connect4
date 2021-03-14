# Required in order to type hint a method with the type of the enclosing class.
# See https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class.
from __future__ import annotations

from connect_four.agents.agent import Agent

from connect_four.evaluation import Evaluator
from connect_four.evaluation.evaluator import ProofStatus
from connect_four.evaluation.tic_tac_toe_simple_evaluator import NodeType


class PNSNode:
    def __init__(self, node_type: NodeType):
        self.status = ProofStatus.Unknown
        self.proof = 1
        self.disproof = 1
        self.children = {}
        self.node_type = node_type

    def __eq__(self, other):
        if isinstance(other, PNSNode):
            return (self.status == other.status and
                    self.proof == other.proof and
                    self.disproof == other.disproof and
                    self.children == other.children and
                    self.node_type == other.node_type)

    def update_tree(self, evaluator: Evaluator):
        # Base case.
        if not self.children:
            self.expand(evaluator=evaluator)
            self.set_proof_and_disproof_numbers()

        pass

    def set_proof_and_disproof_numbers(self):
        if self.children:
            if self.node_type == NodeType.AND:
                pass
            else:  # self.node_type == NodeType.OR
                # Proof number is the smallest proof number of any child.
                self.proof = float('inf')
                # Disproof number is the sum disproof number of all children.
                self.disproof = 0

                for action in self.children:
                    child = self.children[action]
                    self.disproof += child.disproof
                    if child.proof < self.proof:
                        self.proof = child.proof
        else:  # self is a terminal or non-terminal leaf.
            if self.status == ProofStatus.Disproven:
                self.proof = float('inf')
                self.disproof = 0
            elif self.status == ProofStatus.Proven:
                self.proof = 0
                self.disproof = float('inf')
            else:  # self.status == ProofStatus.Disproven
                self.proof = 1
                self.disproof = 1

    def expand(self, evaluator: Evaluator):
        for action in range(evaluator.action_space):
            # Create the child node.
            child = self._create_child(action=action)

            # Evaluate the child node.
            evaluator.move(action=action)
            child.status = evaluator.evaluate()
            evaluator.undo_move()

            # Set the proof and disproof numbers of the child node.
            child.set_proof_and_disproof_numbers()

            # Break early based on the NodeType (OR/AND).
            if ((self.node_type == NodeType.OR and child.proof == 0) or
                    (self.node_type == NodeType.AND and child.disproof == 0)):
                return

    def _create_child(self, action: int) -> PNSNode:
        if self.node_type == NodeType.OR:
            self.children[action] = PNSNode(node_type=NodeType.AND)
        else:  # self.node_type == NodeType.AND
            self.children[action] = PNSNode(node_type=NodeType.OR)
        return self.children[action]

    def select_most_proving_child(self) -> (int, PNSNode):
        value = float('inf')
        best_action = -1
        if self.node_type == NodeType.OR:
            # Select the child with the smallest proof number.
            for action in self.children:
                child = self.children[action]
                if value > child.proof:
                    best_action = action
                    value = child.proof
        else:  # self.node_type == NodeType.AND
            # Select the child with the smallest disproof number.
            for action in self.children:
                child = self.children[action]
                if value > child.disproof:
                    best_action = action
                    value = child.disproof
        return best_action, self.children[best_action]


class PNS(Agent):
    def action(self, env, last_action=None):
        pass
