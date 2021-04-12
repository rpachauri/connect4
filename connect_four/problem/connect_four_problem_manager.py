from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.problem.connecting_problem_manager import ConnectingProblemManager


class ConnectFourProblemManager(ConnectingProblemManager):
    def __init__(self, env_variables: TwoPlayerGameEnvVariables):
        super().__init__(env_variables, num_to_connect=4)
