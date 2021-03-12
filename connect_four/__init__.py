from gym.envs.registration import register

register(
    id='connect_four-v0',
    entry_point='connect_four.envs:ConnectFourEnv',
)

register(
    id='tic_tac_toe-v0',
    entry_point='connect_four.envs:TicTacToeEnv',
)
