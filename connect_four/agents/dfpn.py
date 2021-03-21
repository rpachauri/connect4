from connect_four.agents.agent import Agent
from connect_four.envs import TwoPlayerGameEnv
from connect_four.evaluation import ProofStatus
from connect_four.evaluation.evaluator import NodeType


class DFPN(Agent):

    def __init__(self):
        pass

    def depth_first_proof_number_search(self, env: TwoPlayerGameEnv) -> ProofStatus:
        """Performs depth-first proof-number search on the state env is currently in to (dis)prove the state.

        Args:
            env (TwoPlayerGameEnv): a TwoPlayerGameEnv instance currently at root. It will be left in its given state.

        Returns:
            status (ProofStatus): the ProofStatus (Proven or Disproven) of the state env is currently in.
        """
        pass

    def multiple_iterative_deepening(self, env: TwoPlayerGameEnv,
                                     phi_threshold: int, delta_threshold: int) -> (int, int):
        """Performs iterative deepening continuously to update the phi/delta numbers of the state env is currently in
        until either of the numbers exceed their respective thresholds. This is known as the "termination condition".
        Saves and returns the phi/delta numbers when the termination condition is satisfied.

        Args:
            env (TwoPlayerGameEnv): a TwoPlayerGameEnv instance. It will be left in its given state.
            phi_threshold (int): The maximum phi number of the current state before we start searching a sibling node.
            delta_threshold: The maximum delta number of the current state before we start searching a sibling node.

        Returns:
            phi (int): the most recent phi number of the state at env.
            delta (int): the most recent delta number of the state at env.
        """
        pass

    def determine_phi_delta(self, node_type: NodeType, status: ProofStatus) -> (int, int):
        """Determines the phi/delta numbers of a (dis)proven AND/OR Node.

        Args:
            node_type (NodeType): either NodeType.OR or NodeType.AND.
            status (ProofStatus): either ProofStatus.Proven or ProofStatus.Disproven.

        Returns:
            phi (int): The phi number.
            delta (int): The delta number.
        """
        pass

    def calculate_phi_delta(self, env: TwoPlayerGameEnv) -> (int, int):
        """Calculates the phi/delta numbers of the state env is currently in base on the phi/delta numbers of
        the state's children.

        Args:
            env (TwoPlayerGameEnv): a TwoPlayerGameEnv instance. It will be left in its given state.

        Returns:
            phi (int): The phi number for the state env is currently in, calculated from its children.
            delta (int): The delta number for the state env is currently in, calculated from its children.
        """
        pass

    def select_child(self, env: TwoPlayerGameEnv) -> (int, int, int):
        """Selects the best action from the given state along with some metadata.

        Args:
            env (TwoPlayerGameEnv): a TwoPlayerGameEnv instance. It will be left in its given state.

        Returns:
            best_action (int): The action that leads to the best child.
            phi_c (int): The phi number of the best child.
            delta_2 (int): The second smallest delta number that belongs to a child of the given state.
        """
        pass

    def action(self, env, last_action=None):
        """
        Requires:
            1. env is not currently at a terminal state.

        Args:
            env (TwoPlayerGameEnv): a TwoPlayerGameEnv instance. It will be left in its given state.
            last_action (int): The last action that occurred in env. None if env is in the initial state.

        Returns:
            best_action (int): an action.
        """
        pass
