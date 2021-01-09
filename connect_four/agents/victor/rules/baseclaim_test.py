import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Baseclaim
from connect_four.agents.victor.rules import find_all_baseclaims

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestBaseclaim(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_baseclaim(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 1, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [1, 0, 0, 0, 0, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_baseclaims = find_all_baseclaims(board)

        # Directly playable squares.
        square_4_0 = Square(row=4, col=0)
        square_5_1 = Square(row=5, col=1)
        square_5_2 = Square(row=5, col=2)
        square_0_3 = Square(row=0, col=3)
        square_5_4 = Square(row=5, col=4)
        square_4_5 = Square(row=4, col=5)
        square_4_6 = Square(row=4, col=6)

        want_baseclaims = {
            ## Baseclaims where square_5_1 is the second square.
            # Baseclaims where square_4_0 is the first square.
            Baseclaim(first=square_4_0, second=square_5_1, third=square_5_2),
            Baseclaim(first=square_4_0, second=square_5_1, third=square_0_3),
            Baseclaim(first=square_4_0, second=square_5_1, third=square_5_4),
            Baseclaim(first=square_4_0, second=square_5_1, third=square_4_5),
            Baseclaim(first=square_4_0, second=square_5_1, third=square_4_6),
            # Baseclaims where square_4_6 is the first square.
            Baseclaim(first=square_4_6, second=square_5_1, third=square_5_2),
            Baseclaim(first=square_4_6, second=square_5_1, third=square_0_3),
            Baseclaim(first=square_4_6, second=square_5_1, third=square_5_4),
            Baseclaim(first=square_4_6, second=square_5_1, third=square_4_5),
            # Baseclaims where square_4_5 is the first square.
            Baseclaim(first=square_4_5, second=square_5_1, third=square_5_2),
            Baseclaim(first=square_4_5, second=square_5_1, third=square_0_3),
            Baseclaim(first=square_4_5, second=square_5_1, third=square_5_4),
            # Baseclaims where square_5_4 is the first square.
            Baseclaim(first=square_5_4, second=square_5_1, third=square_5_2),
            Baseclaim(first=square_5_4, second=square_5_1, third=square_0_3),
            # Baseclaims where square_0_3 is the first square.
            Baseclaim(first=square_0_3, second=square_5_1, third=square_5_2),

            ## Baseclaims where square_5_2 is the second square.
            # Baseclaims where square_5_1 is the first square.
            Baseclaim(first=square_5_1, second=square_5_2, third=square_0_3),
            Baseclaim(first=square_5_1, second=square_5_2, third=square_5_4),
            Baseclaim(first=square_5_1, second=square_5_2, third=square_4_5),
            Baseclaim(first=square_5_1, second=square_5_2, third=square_4_6),
            Baseclaim(first=square_5_1, second=square_5_2, third=square_4_0),
            # Baseclaims where square_4_0 is the first square.
            Baseclaim(first=square_4_0, second=square_5_2, third=square_0_3),
            Baseclaim(first=square_4_0, second=square_5_2, third=square_5_4),
            Baseclaim(first=square_4_0, second=square_5_2, third=square_4_5),
            Baseclaim(first=square_4_0, second=square_5_2, third=square_4_6),
            # Baseclaims where square_4_6 is the first square.
            Baseclaim(first=square_4_6, second=square_5_2, third=square_0_3),
            Baseclaim(first=square_4_6, second=square_5_2, third=square_5_4),
            Baseclaim(first=square_4_6, second=square_5_2, third=square_4_5),
            # Baseclaims where square_4_5 is the first square.
            Baseclaim(first=square_4_5, second=square_5_2, third=square_0_3),
            Baseclaim(first=square_4_5, second=square_5_2, third=square_5_4),
            # Baseclaims where square_5_4 is the first square.
            Baseclaim(first=square_5_4, second=square_5_2, third=square_0_3),

            ## Baseclaims where square_5_4 is the second square.
            # Baseclaims where square_0_3 is the first square.
            Baseclaim(first=square_0_3, second=square_5_4, third=square_4_5),
            Baseclaim(first=square_0_3, second=square_5_4, third=square_4_6),
            Baseclaim(first=square_0_3, second=square_5_4, third=square_4_0),
            Baseclaim(first=square_0_3, second=square_5_4, third=square_5_1),
            Baseclaim(first=square_0_3, second=square_5_4, third=square_5_2),
            # Baseclaims where square_5_2 is the first square.
            Baseclaim(first=square_5_2, second=square_5_4, third=square_4_5),
            Baseclaim(first=square_5_2, second=square_5_4, third=square_4_6),
            Baseclaim(first=square_5_2, second=square_5_4, third=square_4_0),
            Baseclaim(first=square_5_2, second=square_5_4, third=square_5_1),
            # Baseclaims where square_5_1 is the first square.
            Baseclaim(first=square_5_1, second=square_5_4, third=square_4_5),
            Baseclaim(first=square_5_1, second=square_5_4, third=square_4_6),
            Baseclaim(first=square_5_1, second=square_5_4, third=square_4_0),
            # Baseclaims where square_4_0 is the first square.
            Baseclaim(first=square_4_0, second=square_5_4, third=square_4_5),
            Baseclaim(first=square_4_0, second=square_5_4, third=square_4_6),
            # Baseclaims where square_4_6 is the first square.
            Baseclaim(first=square_4_6, second=square_5_4, third=square_4_5),
        }
        self.assertEqual(want_baseclaims, got_baseclaims)


if __name__ == '__main__':
    unittest.main()
