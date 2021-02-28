from enum import Enum

from connect_four.agents.agent import Agent
from connect_four.agents.victor.planning import plan_initializer


class ProofStatus(Enum):
    exploring = 0
    winning = 1
    drawing = 2
    losing = 3


class VictorNode:
    def __init__(self):
        self.actions_to_children = {}  # dictionary of actions to VictorNodes.
        self.status = ProofStatus.exploring  # Every node is initialized with a status of exploring.
        self.solution_found = False  # Whether or not a solution has been found using the evaluator.

    def best_action(self):
        # Assumes all actions have been explored and each has a status in {winning, drawing, losing}.
        # Find an action that causes the other player to be in a "losing" state.
        for action in self.actions_to_children:
            if self.actions_to_children[action].status == ProofStatus.losing:
                return action

        # At this point, all actions have a status in {winning, drawing}.
        # Find an action that causes the other player to be in a "drawing" state.
        for action in self.actions_to_children:
            if self.actions_to_children[action].status == ProofStatus.drawing:
                return action

        # Return any action.
        return list(self.actions_to_children.keys())[0]


def proof_number_search(node: VictorNode):
    node.solution_found = True


class Victor(Agent):
    def __init__(self):
        self.root = None
        self.plan = None

    def action(self, env, last_action=None):
        if self.root is None:
            self.root = VictorNode()
            proof_number_search(self.root)

        # Execute the "Search-Tree" mode.
        if not self.root.solution_found:
            best_move = self.root.best_action()
            self.root = self.root.actions_to_children[best_move]
            return best_move

        # Execute the "Plan" mode.
        if self.plan is None:
            env.undo_last_action(action=last_action)
            self.plan = plan_initializer.PlanWrapper(env)
            env.step(action=last_action)

        return self.plan.execute(last_action)
