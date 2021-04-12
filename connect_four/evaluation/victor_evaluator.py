from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.evaluator import evaluator
from connect_four.envs import ConnectFourEnv
from connect_four.evaluation import ProofStatus, NodeType
from connect_four.evaluation.simple_evaluator import SimpleEvaluator
from connect_four.evaluation.victor.graph.graph_manager import GraphManager
from connect_four.evaluation.victor.solution import VictorSolutionManager
from connect_four.problem import ConnectFourProblemManager


class Victor(SimpleEvaluator):

    def __init__(self, model: ConnectFourEnv):
        super().__init__(model=model)

    def evaluate(self) -> ProofStatus:
        proof_status = super().evaluate()
        if proof_status != ProofStatus.Unknown:
            return proof_status

        problem_manager = ConnectFourProblemManager(env_variables=self.model.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.model.env_variables)
        graph_manager = GraphManager(
            player=self.model.env_variables.player_turn,
            problem_manager=problem_manager,
            solution_manager=solution_manager,
        )
        evaluation = graph_manager.evaluate()

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
