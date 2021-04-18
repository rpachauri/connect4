from connect_four.envs import ConnectFourEnv
from connect_four.evaluation import ProofStatus, NodeType
from connect_four.evaluation.simple_evaluator import SimpleEvaluator
from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.graph.graph_manager import GraphManager
from connect_four.evaluation.victor.solution import VictorSolutionManager
from connect_four.problem import ConnectFourProblemManager


class IncrementalVictor(SimpleEvaluator):

    def __init__(self, model: ConnectFourEnv):
        super().__init__(model=model)
        problem_manager = ConnectFourProblemManager(env_variables=self.model.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.model.env_variables)
        self.graph_manager = GraphManager(
            player=self.model.env_variables.player_turn,
            problem_manager=problem_manager,
            solution_manager=solution_manager,
        )
        self.reached_terminal_state = False

    def move(self, action: int):
        """
        Modifies:
            -   This Evaluator's model will be at the resulting state.

        Args:
            action (int): an action that can be applied in the current state of this evaluator's model environment.
        """
        super().move(action=action)

        if self.done:
            self.reached_terminal_state = True
        else:
            board = Board(env_variables=self.model.env_variables)
            row = 0
            playable_square = board.playable_square(col=action)
            if playable_square is not None:
                row = playable_square.row + 1

            self.model.render()
            self.graph_manager.move(row=row, col=action)

    def undo_move(self):
        super().undo_move()

        if self.reached_terminal_state:
            self.reached_terminal_state = False
        else:
            self.graph_manager.undo_move()

    def evaluate(self) -> ProofStatus:
        # self.model.render()

        proof_status = super().evaluate()
        if proof_status != ProofStatus.Unknown:
            return proof_status

        evaluation = self.graph_manager.evaluate()

        # board = Board(env_variables=self.model.env_variables)
        # evaluation = evaluator.evaluate(board=board)
        if evaluation is not None:
            if self.node_type == NodeType.OR:
                # If it is White's turn and the evaluation is not None,
                # then Black has found a way to disprove this node.
                return ProofStatus.Disproven
            else:
                # If it is Black's turn and the evaluation is not None,
                # then White has found a way to prove this node.
                return ProofStatus.Proven

        # If the evaluation is None, then this state is unknown.
        return ProofStatus.Unknown
