from connect_four.envs import TwoPlayerGameEnv
from connect_four.evaluation import ProofStatus, NodeType
from connect_four.evaluation.simple_evaluator import SimpleEvaluator


class Depth1Evaluator(SimpleEvaluator):
    def evaluate(self) -> ProofStatus:
        proof_status = super().evaluate()
        if proof_status != ProofStatus.Unknown:
            return proof_status

        env_variables = self.model.env_variables
        for action in self.actions():
            _, reward, done, _ = self.model.step(action=action)
            if done and reward == TwoPlayerGameEnv.CONNECTED:
                if self.node_type == NodeType.OR:
                    proof_status = ProofStatus.Proven
                else:
                    proof_status = ProofStatus.Disproven
            self.model.reset(env_variables=env_variables)
        return proof_status
