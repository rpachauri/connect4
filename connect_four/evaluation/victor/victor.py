from enum import Enum

from connect_four.agents.agent import Agent
from connect_four.evaluation.victor import Board
from connect_four.evaluation.victor.planning import plan_initializer
from connect_four.evaluation.victor.evaluator import evaluator
from connect_four.envs import ConnectFourEnv


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


def proof_number_search(node: VictorNode, env):
    env_variables = env.env_variables
    board = Board(env_variables=env_variables)

    for action in range(env.action_space):
        # Assumes node.actions_to_children is empty.
        node.actions_to_children[action] = VictorNode()
        child = node.actions_to_children[action]

        _, reward, done, _ = env.step(action=action)  # env is now at child.
        env.reset(env_variables=env_variables)  # Immediately reset the environment.

        if done:
            child.status = terminal_state_reward_to_opponent_status(reward=reward)

            # If the action leads to a loss for the other player,
            # then this state is solved because we only need to pick that action.
            if child.status == ProofStatus.losing:
                node.status = ProofStatus.winning
                return

            # If the action leads to a draw and the current player is Black, then this state is solved.
            if board.player == 1 and child.status == ProofStatus.drawing:
                node.status = ProofStatus.drawing
                return

            # status = player_goal_to_status(reward=reward, player=env.player_turn)
            # if status != ProofStatus.exploring:  # Player has found an outcome they're happy with.
            #     node.status = status
            #     return
    # TODO What happens if an action leads to ConnectFourEnv.INVALID_MOVE?
    # TODO if all the actions lead to a terminal loss, end early

    evaluation = evaluator.evaluate(board=board)
    if evaluation is not None:
        node.solution_found = True
        if board.player == 0:  # White to move. Black has found a solution, guaranteeing themselves a draw.
            node.status = ProofStatus.drawing
        else:  # Black to move. White has found a solution, guaranteeing themselves a win.
            node.status = ProofStatus.losing
        return

    # Assumes node.children is empty. TODO remove?
    for action in range(env.action_space):
        # child = VictorNode()
        # node.actions_to_children[action] = child
        child = node.actions_to_children[action]

        # Only explore nodes that are still exploring.
        if child.status == ProofStatus.exploring:

            _, reward, done, _ = env.step(action=action)  # env is now at child.
            proof_number_search(child, env)  # Explore child.
            env.reset(env_variables=env_variables)
            # child now has a status in {winning, drawing, losing}.

            # If the action leads to a loss for the other player,
            # then this state is solved because we only need to pick that action.
            if child.status == ProofStatus.losing:
                node.status = ProofStatus.winning
                return

            # If the action leads to a draw and the current player is Black, then this state is solved.
            if board.player == 1 and child.status == ProofStatus.drawing:
                node.status = ProofStatus.drawing
                return

    # At this point, all children have been explored.
    # For White, every child has a status in {winning, drawing}.
    # For Black, every child has a status of {winning}.
    for action in node.actions_to_children:
        child = node.actions_to_children[action]
        if child.status == ProofStatus.drawing:
            node.status = ProofStatus.drawing
            return

    # At this point, all children have a status of {winning}, meaning that no matter what
    # the current player plays, the opponent is guaranteed to win.
    node.status = ProofStatus.losing
    return


def player_goal_to_status(reward, player):
    # Assumptions:
    #   1. In a given state, there is at least one action that does not lead to an immediate loss for the player.
    #      (i.e. by "immediate loss", we mean a terminal state indicating a loss for the player).

    # Both players are happy winning.
    if reward == ConnectFourEnv.CONNECTED:
        return ProofStatus.winning

    if player == 1 and reward == ConnectFourEnv.DRAW:  # Black is happy with a draw.
        return ProofStatus.drawing

    # If the player hasn't found an outcome they're happy with, they should keep exploring.
    return ProofStatus.exploring


def terminal_state_reward_to_opponent_status(reward):
    if reward == ConnectFourEnv.CONNECTED:
        # If the player has connected four, then this is a losing state for the opponent.
        return ProofStatus.losing

    if reward == ConnectFourEnv.DRAW:
        # If the player has drawn, then this is a drawing state for the opponent.
        return ProofStatus.drawing

    # Assumes the only remaining reward is ConnectFourEnv.INVALID_MOVE.
    # If the player has made an invalid move, then this is a winning state for the opponent.
    return ProofStatus.winning


class Victor(Agent):
    def __init__(self):
        self.root = None
        self.plan = None

    def action(self, env, last_action=None):
        # If we already have a plan, execute according to the plan.
        if self.plan is not None:
            return self.plan.execute(last_action)

        # Try to come up with a Plan.
        env.undo_last_action(action=last_action)
        board = Board(env_variables=env.env_variables)
        evaluation = evaluator.evaluate(board=board)
        env.step(action=last_action)

        if evaluation is not None:
            env.undo_last_action(action=last_action)
            self.plan = plan_initializer.PlanWrapper(env)
            env.step(action=last_action)
            return self.plan.execute(last_action)

        if self.root is None:
            self.root = VictorNode()

            for action in range(env.action_space):
                child = VictorNode()
                self.root.actions_to_children[action] = child

                env.step(action=action)
                proof_number_search(child, env)
                env.undo_last_action(action=action)

                # If the action leads to a loss for the other player,
                # then this state is solved because we only need to pick that action.
                if child.status == ProofStatus.losing:
                    self.root = child
                    return action

                # If the action leads to a draw and the current player is Black, then this state is solved.
                if env.player_turn == 1 and child.status == ProofStatus.drawing:
                    self.root = child
                    return action

        # if self.root is None:
        #     env.undo_last_action(action=last_action)
        #     self.root = VictorNode()
        #     proof_number_search(self.root, env)
        #     env.step(action=last_action)

        if self.root.solution_found:
            # Execute the "Plan" mode.
            if self.plan is None:
                env.undo_last_action(action=last_action)
                self.plan = plan_initializer.PlanWrapper(env)
                env.step(action=last_action)

            return self.plan.execute(last_action)

        # Assumes there is a child node for every action from root.
        # Root points to the state before the opponent made last_action.
        # Move root to the state after opponent moves last_action so that it corresponds with env.
        self.root = self.root.actions_to_children[last_action]

        # Execute the "Search-Tree" mode.
        if not self.root.solution_found:
            # if not self.root.actions_to_children:
            #     print("Hello World")

            best_move = self.root.best_action()
            self.root = self.root.actions_to_children[best_move]
            return best_move
