from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.problem.connecting_group_manager import ConnectingGroupManager


class ConnectFourGroupManager(ConnectingGroupManager):
    def __init__(self, env_variables: TwoPlayerGameEnvVariables):
        super().__init__(env_variables, num_to_connect=4)
