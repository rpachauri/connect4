import gym
import unittest

import numpy as np

from connect_four.agents.victor import Board
from connect_four.agents.victor import Square
from connect_four.agents.victor import Rule
from connect_four.agents.victor import Solution
from connect_four.agents.victor import solution
from connect_four.agents.victor import Threat
from connect_four.agents.victor import threat

from connect_four.agents.victor import Claimeven
from connect_four.agents.victor import Baseinverse

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestSolution(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_claimeven(self):
        # This board is from Diagram 5.4 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 1, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)

        white_threats = board.potential_threats(0)
        square_to_threats = threat.square_to_threats(white_threats)

        # We're using the Claimeven with the upper square being e4.
        # In the example from the original paper, this refutes the groups in (4):
        # d3-g6, c2-f5, b1-e4, e3-e6
        claimeven_2_4 = Claimeven(upper=Square(row=2, col=4), lower=Square(row=3, col=4))

        got_solution = solution.from_claimeven(claimeven_2_4, square_to_threats)
        want_solution = Solution(
            rule=Rule.Claimeven,
            squares=frozenset([claimeven_2_4.upper, claimeven_2_4.lower]),
            threats=frozenset([
                Threat(player=0, start=Square(row=3, col=3), end=Square(row=0, col=6)),  # d3-g6
                Threat(player=0, start=Square(row=4, col=2), end=Square(row=1, col=5)),  # c2-f5
                Threat(player=0, start=Square(row=5, col=1), end=Square(row=2, col=4)),  # b1-e4
                Threat(player=0, start=Square(row=3, col=4), end=Square(row=0, col=4)),  # e3-d6
            ]),
        )
        self.assertEqual(want_solution, got_solution)

    def test_baseinverse(self):
        # This board is from Diagram 6.2 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)

        white_threats = board.potential_threats(0)
        square_to_threats = threat.square_to_threats(white_threats)

        # The Baseinverse a1-b1 solves a1-d1.
        baseinverse_a1_b1 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=5, col=1))

        got_solution = solution.from_baseinverse(baseinverse_a1_b1, square_to_threats)
        want_solution = Solution(
            rule=Rule.Baseinverse,
            squares=frozenset(baseinverse_a1_b1.squares),
            threats=frozenset([
                Threat(player=0, start=Square(row=5, col=0), end=Square(row=5, col=3)),
            ]),
        )
        self.assertEqual(want_solution, got_solution)

        # As stated in the original paper, the Baseinverse a1-c4 is possible but useless.
        # Thus, it should not be converted into a Solution.
        baseinverse_a1_c4 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=2, col=2))
        self.assertIsNone(solution.from_baseinverse(baseinverse_a1_c4, square_to_threats))


if __name__ == '__main__':
    unittest.main()
