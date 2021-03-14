from enum import Enum

from connect_four.envs import TwoPlayerGameEnv
from connect_four.evaluation import Evaluator, ProofStatus


class NodeType(Enum):
    OR = 0
    AND = 1


class TicTacToeSimpleEvaluator(Evaluator):
    def __init__(self, model: TwoPlayerGameEnv, node_type: NodeType):
        """
        Requires:
            model's current state cannot be a terminal state.

        Args:
            model (TwoPlayerGameEnv): a TwoPlayerGameEnv instance that can be modified.
        """
        super().__init__(model)
        self.model = model
        self.list_of_env_variables = []
        self.reward = TwoPlayerGameEnv.DEFAULT_REWARD
        self.done = False
        self.node_type = node_type

    def move(self, action: int):
        """
        Modifies:
            -   This Evaluator's model will be at the resulting state.

        Args:
            action (int): an action that can be applied in the current state of this evaluator's model environment.
        """
        assert not self.done

        self.list_of_env_variables.append(self.model.env_variables)
        _, self.reward, self.done, _ = self.model.step(action=action)
        self._switch_play()

    def undo_move(self):
        env_variables = self.list_of_env_variables.pop()
        self.model.reset(env_variables=env_variables)
        self.reward = TwoPlayerGameEnv.DEFAULT_REWARD
        self.done = False
        self._switch_play()

    def _switch_play(self):
        if self.node_type == NodeType.OR:
            self.node_type = NodeType.AND
        else:  # self.node_type == NodeType.AND
            self.node_type = NodeType.OR

    def evaluate(self) -> ProofStatus:
        if not self.done:
            # The game is not yet done.
            return ProofStatus.Unknown

        # The game has ended, so we must be able to either Prove or Disprove this node.
        if self.node_type == NodeType.AND:
            # Player OR has connected three, indicating this node is proven.
            if self.reward == TwoPlayerGameEnv.CONNECTED:
                return ProofStatus.Proven

            # The game has ended without player OR connecting three. This node is disproven.
            return ProofStatus.Disproven

        # self.node_type == NodeType.OR
        # Player AND has played an invalid move, resulting in a win for OR, indicating this node is proven.
        if self.reward == TwoPlayerGameEnv.INVALID_MOVE:
            return ProofStatus.Proven

        # The game has ended without AND losing, so OR has failed to prove this node.
        return ProofStatus.Disproven
