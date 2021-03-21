import copy
from connect_four.envs import TwoPlayerGameEnv
from connect_four.evaluation import Evaluator, ProofStatus
from connect_four.evaluation.evaluator import NodeType
from typing import Sequence


class TicTacToeSimpleEvaluator(Evaluator):
    def __init__(self, model: TwoPlayerGameEnv, node_type: NodeType):
        """
        Requires:
            model's current state cannot be a terminal state.

        Args:
            model (TwoPlayerGameEnv): a TwoPlayerGameEnv instance that can be modified.
        """
        super().__init__(node_type=node_type)
        self.model = copy.deepcopy(model)
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
        super().move(action=action)

        assert not self.done

        self.list_of_env_variables.append(self.model.env_variables)
        _, self.reward, self.done, _ = self.model.step(action=action)

    def undo_move(self):
        super().undo_move()

        env_variables = self.list_of_env_variables.pop()
        self.model.reset(env_variables=env_variables)
        self.reward = TwoPlayerGameEnv.DEFAULT_REWARD
        self.done = False

    def evaluate(self) -> ProofStatus:
        if not self.done:
            # The game is not yet done.
            return ProofStatus.Unknown

        # The game has ended, so we must be able to either Prove or Disprove this node.
        # Player OR has connected three, indicating this node is proven.
        if self.node_type == NodeType.AND and self.reward == TwoPlayerGameEnv.CONNECTED:
            return ProofStatus.Proven

        # The game has ended without OR winning, so OR has failed to prove this node.
        return ProofStatus.Disproven

    def actions(self) -> Sequence[int]:
        return self.model.actions()

    @property
    def state(self):
        return self.model.state
