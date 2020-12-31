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
from connect_four.agents.victor import Vertical
from connect_four.agents.victor import Aftereven
from connect_four.agents.victor import Lowinverse

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
                Threat(player=0, start=Square(row=5, col=0), end=Square(row=5, col=3)),  # a1-d1
            ]),
        )
        self.assertEqual(want_solution, got_solution)

        # As stated in the original paper, the Baseinverse a1-c4 is possible but useless.
        # Thus, it should not be converted into a Solution.
        baseinverse_a1_c4 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=2, col=2))
        self.assertIsNone(solution.from_baseinverse(baseinverse_a1_c4, square_to_threats))

    def test_from_vertical(self):
        # This board is from Diagram 6.3 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)

        white_threats = board.potential_threats(0)
        square_to_threats = threat.square_to_threats(white_threats)

        # The Vertical e4-e5 solves e2-e5 and e3-e6.
        vertical_e4_e5 = Vertical(upper=Square(row=2, col=4), lower=Square(row=3, col=4))

        got_solution = solution.from_vertical(vertical_e4_e5, square_to_threats)
        want_solution = Solution(
            rule=Rule.Vertical,
            squares=frozenset([vertical_e4_e5.upper, vertical_e4_e5.lower]),
            threats=frozenset([
                Threat(player=0, start=Square(row=4, col=4), end=Square(row=1, col=4)),  # e2-e5
                Threat(player=0, start=Square(row=3, col=4), end=Square(row=0, col=4)),  # e3-e6
            ])
        )
        self.assertEqual(want_solution, got_solution)

    def test_aftereven(self):
        # This board is from Diagram 6.5 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 1, 1, 0, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [1, 0, 0, 1, 1, 0, 0, ],
                [1, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)

        white_threats = board.potential_threats(0)
        square_to_threats = threat.square_to_threats(white_threats)

        # The Aftereven d2-g2 solves all groups which need a square in both the f and g column.
        aftereven_d2_g2 = Aftereven(
            threat=Threat(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
            claimevens=[
                Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5)),  # Claimeven f1-f2
                Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6)),  # Claimeven g1-g2
            ],
        )

        got_solution = solution.from_aftereven(aftereven_d2_g2, square_to_threats)
        want_solution = Solution(
            rule=Rule.Aftereven,
            squares=frozenset([
                # Squares from d2-g2.
                Square(row=4, col=3),
                Square(row=4, col=4),
                Square(row=4, col=5),
                Square(row=4, col=6),
                # Lower squares of Claimevens.
                Square(row=5, col=5),
                Square(row=5, col=6),
            ]),
            threats=frozenset([
                # New threats from Aftereven.
                Threat(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6)),  # d3-g3
                Threat(player=0, start=Square(row=1, col=3), end=Square(row=1, col=6)),  # d5-g5
                Threat(player=0, start=Square(row=0, col=3), end=Square(row=0, col=6)),  # d6-g6
                Threat(player=0, start=Square(row=0, col=3), end=Square(row=3, col=6)),  # d0-g3
                # Threats refuted by Claimeven f1-f2.
                Threat(player=0, start=Square(row=2, col=5), end=Square(row=5, col=5)),  # f1-f4
                Threat(player=0, start=Square(row=1, col=5), end=Square(row=4, col=5)),  # f2-f5
                # Threats refuted by Claimeven g1-g2.
                Threat(player=0, start=Square(row=2, col=6), end=Square(row=5, col=6)),  # g1-g4
                Threat(player=0, start=Square(row=1, col=6), end=Square(row=4, col=6)),  # g2-g5
            ]),
        )
        for got_threat in got_solution.threats:
            print(got_threat.squares)
        self.assertEqual(want_solution, got_solution)

    def test_lowinverse(self):
        # This board is from Diagram 6.6 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)

        white_threats = board.potential_threats(0)
        square_to_threats = threat.square_to_threats(white_threats)

        # Lowinverse c2-c3-d2-d3 guarantees that Black will get at least one square
        # out of each of three pairs of squares:
        # 1. The squares in the first column (c2-c3).
        # 2. The squares in the other column (d2-d3).
        # 3. The upper two squares (c3-d3).
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2)),  # c2-c3
            second_vertical=Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3)),  # d2-d3
        )

        got_solution = solution.from_lowinverse(lowinverse_c2_c3_d2_d3, square_to_threats)
        want_solution = Solution(
            rule=Rule.Lowinverse,
            squares=frozenset([
                Square(row=3, col=2),
                Square(row=4, col=2),
                Square(row=3, col=3),
                Square(row=4, col=3),
            ]),
            threats=frozenset([
                # Threats which contain both upper squares of the Verticals.
                Threat(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
                Threat(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
                Threat(player=0, start=Square(row=3, col=2), end=Square(row=3, col=5)),  # c3-f3
                # Threats refuted by Vertical c2-c3.
                Threat(player=0, start=Square(row=1, col=2), end=Square(row=4, col=2)),  # c2-c5
                # Note that c1-c4 does not need to be refuted because Black already occupies c1.
                # Threats refuted by Vertical d2-d3.
                Threat(player=0, start=Square(row=1, col=3), end=Square(row=4, col=3)),  # d2-d5
                Threat(player=0, start=Square(row=2, col=3), end=Square(row=5, col=3)),  # d1-d4
            ]),
        )
        self.assertEqual(want_solution, got_solution)


if __name__ == '__main__':
    unittest.main()
