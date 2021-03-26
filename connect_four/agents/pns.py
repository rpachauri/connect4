# Required in order to type hint a method with the type of the enclosing class.
# See https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class.
from __future__ import annotations

from connect_four.agents.agent import Agent

from connect_four.evaluation import Evaluator
from connect_four.evaluation.evaluator import ProofStatus, NodeType


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
            return

        # Recursive case.
        old_proof = self.proof
        old_disproof = self.disproof
        while self.proof == old_proof and self.disproof == old_disproof:
            action, most_proving_child = self.select_most_proving_child()
            evaluator.move(action)
            most_proving_child.update_tree(evaluator=evaluator)
            evaluator.undo_move()

            old_proof = self.proof
            old_disproof = self.disproof
            self.set_proof_and_disproof_numbers()

    def set_proof_and_disproof_numbers(self):
        if self.children:
            if self.node_type == NodeType.AND:
                # Proof number is the sum proof number of all children.
                self.proof = 0
                # Disproof number is the smallest disproof number of any child.
                self.disproof = float('inf')

                for action in self.children:
                    child = self.children[action]
                    self.proof += child.proof
                    if child.disproof < self.disproof:
                        self.disproof = child.disproof

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
        for action in evaluator.actions():
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
        best_action = 0
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
    def __init__(self, evaluator: Evaluator):
        self.evaluator = evaluator
        self.root = PNSNode(evaluator.node_type)
        self.root.update_tree(evaluator=self.evaluator)

    def action(self, env, last_action=None):
        """
        Requires:
            1. env is not currently at a terminal state.

        Args:
            env (TwoPlayerGameEnv): a TwoPlayerGameEnv instance. It will not be modified.
            last_action (int): The last action that occurred in env. None if env is in the initial state.

        Returns:
            best_action (int): an action.
        """
        if last_action is not None:
            # Assumes:
            #  Since env is not currently at a terminal state, if last_action is not None,
            #  this should not cause problems when moving self.evaluator and self.root.
            self.evaluator.move(action=last_action)
            self.root = self.root.children[last_action]

        while self.root.proof != 0 and self.root.disproof != 0:
            self.root.update_tree(evaluator=self.evaluator)

        best_action, best_child = self.root.select_most_proving_child()
        self.evaluator.move(action=best_action)
        self.root = best_child

        return best_action
