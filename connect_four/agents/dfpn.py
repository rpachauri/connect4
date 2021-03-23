from connect_four.agents.agent import Agent
from connect_four.envs import TwoPlayerGameEnv
from connect_four.evaluation import ProofStatus, NodeType, Evaluator
from connect_four.transposition import TranspositionTable


class DFPN(Agent):
    # Python 3 doesn't have an infinity for ints. It does have one for floats, but that led to messy
    # code (in terms of type hints). This constant is a large enough int that no node should ever reach
    # a (dis)proof number this high.
    INF = 100000000000000

    def __init__(self, evaluator: Evaluator, tt: TranspositionTable):
        self.evaluator = evaluator
        self.tt = tt

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
            phi_threshold (int): Maximum phi number of the current state before we start searching a sibling node.
            delta_threshold (int): Maximum delta number of the current state before we start searching a sibling node.

        Returns:
            phi (int): the most recent phi number of the state at env.
            delta (int): the most recent delta number of the state at env.
        """
        env_variables = env.env_variables
        state = env_variables[0]

        self.generate_children()
        phi, delta = self.calculate_phi_delta(env=env)

        while phi_threshold > phi and delta_threshold > delta:
            best_action, phi_c, delta_2 = self.select_child(env=env)

            env.step(action=best_action)
            self.evaluator.move(action=best_action)

            child_phi_threshold = delta_threshold - delta + phi_c
            child_delta_threshold = min(phi_threshold, delta_2 + 1)
            self.multiple_iterative_deepening(
                env=env,
                phi_threshold=child_phi_threshold,
                delta_threshold=child_delta_threshold,
            )

            env.reset(env_variables=env_variables)
            self.evaluator.undo_move()

            phi, delta = self.calculate_phi_delta(env=env)

        self.tt.save(state=state, phi=phi, delta=delta)
        return phi, delta

    @staticmethod
    def determine_phi_delta(node_type: NodeType, status: ProofStatus) -> (int, int):
        """Determines the phi/delta numbers of a (dis)proven AND/OR Node.

        Args:
            node_type (NodeType): either NodeType.OR or NodeType.AND.
            status (ProofStatus): either ProofStatus.Proven or ProofStatus.Disproven.

        Returns:
            phi (int): The phi number.
            delta (int): The delta number.
        """
        if ((node_type == NodeType.OR and status == ProofStatus.Proven) or
                (node_type == NodeType.AND and status == ProofStatus.Disproven)):
            # If an OR node has been proven or an AND node has been disproven, it has reached its goal.
            return 0, DFPN.INF

        # If an OR node has been disproven or an AND node has been proven, it will never reach its goal.
        return DFPN.INF, 0

    def generate_children(self):
        for action in self.evaluator.actions():
            self.evaluator.move(action=action)
            status = self.evaluator.evaluate()

            if status != ProofStatus.Unknown:
                phi, delta = self.determine_phi_delta(node_type=self.evaluator.node_type, status=status)
                self.tt.save(state=self.evaluator.state, phi=phi, delta=delta)
            elif self.evaluator.state not in self.tt:  # ProofStatus is unknown and the state isn't already in the TT.
                self.tt.save(state=self.evaluator.state, phi=1, delta=1)

            self.evaluator.undo_move()

    def calculate_phi_delta(self, env: TwoPlayerGameEnv) -> (int, int):
        """Calculates the phi/delta numbers of the state env is currently in base on the phi/delta numbers of
        the state's children.

        Args:
            env (TwoPlayerGameEnv): a TwoPlayerGameEnv instance. It will be left in its given state.

        Returns:
            phi (int): The phi number for the state env is currently in, calculated from its children.
            delta (int): The delta number for the state env is currently in, calculated from its children.
        """
        min_delta_of_children = DFPN.INF
        sum_phi_of_children = 0

        env_variables = env.env_variables
        for action in env.actions():
            obs, _, _, _ = env.step(action=action)

            child_phi, child_delta = self.tt.retrieve(state=obs)
            sum_phi_of_children += child_phi
            min_delta_of_children = min(min_delta_of_children, child_delta)

            env.reset(env_variables=env_variables)

        return min_delta_of_children, sum_phi_of_children

    def select_child(self, env: TwoPlayerGameEnv) -> (int, int, int):
        """Selects the best action from the given state along with some metadata.

        Args:
            env (TwoPlayerGameEnv): a TwoPlayerGameEnv instance. It will be left in its given state.

        Returns:
            best_action (int): The action that leads to the best child.
            phi_c (int): The phi number of the best child.
            delta_2 (int): The second smallest delta number that belongs to a child of the given state.
        """
        best_action = -1
        best_child_phi = DFPN.INF
        second_best_child_delta = DFPN.INF
        best_child_delta = DFPN.INF

        env_variables = env.env_variables
        for action in env.actions():
            obs, _, _, _ = env.step(action=action)

            child_phi, child_delta = self.tt.retrieve(state=obs)
            if child_delta < best_child_delta:
                best_action = action
                best_child_phi = child_phi
                second_best_child_delta = best_child_delta
                best_child_delta = child_delta
            elif child_delta < second_best_child_delta:
                second_best_child_delta = child_delta

            env.reset(env_variables=env_variables)

        return best_action, best_child_phi, second_best_child_delta

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
