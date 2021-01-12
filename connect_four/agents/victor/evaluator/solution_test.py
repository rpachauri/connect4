import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Threat
from connect_four.agents.victor.game import threat

from connect_four.agents.victor.rules import Rule
from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Aftereven
from connect_four.agents.victor.rules import Lowinverse
from connect_four.agents.victor.rules import Highinverse
from connect_four.agents.victor.rules import Baseclaim
from connect_four.agents.victor.rules import Before
from connect_four.agents.victor.rules import Specialbefore

from connect_four.agents.victor.evaluator import Solution
from connect_four.agents.victor.evaluator import solution

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestSolution(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_from_claimeven(self):
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
        square_to_threats = board.potential_threats_by_square()

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
            claimeven_bottom_squares=[claimeven_2_4.lower],
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_baseinverse(self):
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
        square_to_threats = board.potential_threats_by_square()

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
        square_to_threats = board.potential_threats_by_square()

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

    def test_from_aftereven(self):
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
        square_to_threats = board.potential_threats_by_square()

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
            claimeven_bottom_squares=[
                # Lower squares of Claimevens.
                Square(row=5, col=5),
                Square(row=5, col=6),
            ],
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_lowinverse(self):
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
        square_to_threats = board.potential_threats_by_square()

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

    def test_from_highinverse(self):
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
        square_to_threats = board.potential_threats_by_square()

        # Lowinverse c2-c3-d2-d3 guarantees that Black will get at least one square
        # out of each of three pairs of squares:
        # 1. The squares in the first column (c2-c3).
        # 2. The squares in the other column (d2-d3).
        # 3. The upper two squares (c3-d3).
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2)),  # c2-c3
            second_vertical=Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3)),  # d2-d3
        )
        # Highinverse c2-c3-c4-d2-d3-d4 guarantees that Black will get at least one square
        # out of each of four pairs of squares:
        # 1. The upper two squares in the first column (c3-c4).
        # 2. The upper two squares in the second column (d3-d4).
        # 3. The middle squares from both columns (c3-d3).
        # 4. The upper squares from both columns (c4-d4).
        highinverse_c2_c3_c4_d2_d3_d4 = Highinverse(
            lowinverse=lowinverse_c2_c3_d2_d3,
        )
        want_solution = Solution(
            rule=Rule.Highinverse,
            squares=frozenset([
                Square(row=2, col=2),  # c4
                Square(row=3, col=2),  # c3
                Square(row=4, col=2),  # c2
                Square(row=2, col=3),  # d4
                Square(row=3, col=3),  # d3
                Square(row=4, col=3),  # d2
            ]),
            threats=frozenset([
                # Threats which contain the upper squares of both columns.
                Threat(player=0, start=Square(row=2, col=0), end=Square(row=2, col=3)),  # a4-d4
                Threat(player=0, start=Square(row=2, col=1), end=Square(row=2, col=4)),  # b4-e4
                Threat(player=0, start=Square(row=2, col=2), end=Square(row=2, col=5)),  # c4-f4
                # Threats which contain the middle squares of both columns.
                Threat(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
                Threat(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
                Threat(player=0, start=Square(row=3, col=2), end=Square(row=3, col=5)),  # c3-f3
                # Threats refuted by Vertical c3-c4.
                Threat(player=0, start=Square(row=0, col=2), end=Square(row=3, col=2)),  # c3-c6
                Threat(player=0, start=Square(row=1, col=2), end=Square(row=4, col=2)),  # c2-c5
                # Note that c1-c4 does not need to be refuted because Black already occupies c1.
                # Threats refuted by Vertical d3-d4.
                Threat(player=0, start=Square(row=0, col=3), end=Square(row=3, col=3)),  # d3-d6
                Threat(player=0, start=Square(row=1, col=3), end=Square(row=4, col=3)),  # d2-d5
                Threat(player=0, start=Square(row=2, col=3), end=Square(row=5, col=3)),  # d1-d4
            ]),
        )
        got_solution = solution.from_highinverse(
            highinverse=highinverse_c2_c3_c4_d2_d3_d4,
            square_to_threats=square_to_threats,
            directly_playable_squares=board.playable_squares(),
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_highinverse_useful_highinverse_useless_lowinverse(self):
        # This test verifies that a Highinverse is converted into a Solution even when
        # its Lowinverse cannot be converted into one.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 1, 1, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        square_to_threats = board.potential_threats_by_square()

        # Lowinverse c4-c5-d4-d5 does not refute any threats that the
        # Verticals which are part of it don't already refute.
        lowinverse_c4_c5_d4_d5 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=1, col=2), lower=Square(row=2, col=2)),  # c4-c5
            second_vertical=Vertical(upper=Square(row=1, col=3), lower=Square(row=2, col=3)),  # d4-d5
        )
        got_lowinverse_solution = solution.from_lowinverse(
            lowinverse=lowinverse_c4_c5_d4_d5,
            square_to_threats=square_to_threats,
        )
        self.assertIsNone(got_lowinverse_solution)
        # Highinverse c4-c5-c6-d4-d5-d6 guarantees that Black will get at least one square
        # out of each of four pairs of squares:
        # 1. The upper two squares in the first column (c5-c6).
        # 2. The upper two squares in the second column (d5-d6).
        # 3. The middle squares from both columns (c5-d5).
        # 4. The upper squares from both columns (c6-d6).
        highinverse_c4_c5_c6_d4_d5_d6 = Highinverse(
            lowinverse=lowinverse_c4_c5_d4_d5,
        )
        want_highinverse_solution = Solution(
            rule=Rule.Highinverse,
            squares=frozenset([
                Square(row=2, col=2),  # c4
                Square(row=1, col=2),  # c5
                Square(row=0, col=2),  # c6
                Square(row=2, col=3),  # d4
                Square(row=1, col=3),  # d5
                Square(row=0, col=3),  # d6
            ]),
            threats=frozenset([
                # Threats which contain the upper squares of both columns.
                Threat(player=0, start=Square(row=0, col=0), end=Square(row=0, col=3)),  # a6-d6
                Threat(player=0, start=Square(row=0, col=1), end=Square(row=0, col=4)),  # b6-e6
                Threat(player=0, start=Square(row=0, col=2), end=Square(row=0, col=5)),  # c6-f6
                # There are no Threats which contain the middle squares of both columns.
                # Threats refuted by Vertical c5-c6.
                Threat(player=0, start=Square(row=0, col=2), end=Square(row=3, col=2)),  # c3-c6
                # Threats refuted by Vertical d5-d6.
                Threat(player=0, start=Square(row=0, col=3), end=Square(row=3, col=3)),  # d3-d6
            ]),
        )
        got_highinverse_solution = solution.from_highinverse(
            highinverse=highinverse_c4_c5_c6_d4_d5_d6,
            square_to_threats=square_to_threats,
            directly_playable_squares=board.playable_squares(),
        )
        self.assertEqual(want_highinverse_solution, got_highinverse_solution)

    def test_from_highinverse_useless_highinverse_useful_lowinverse(self):
        # This test verifies that a Highinverse is not converted into a Solution
        # if it doesn't create any new potential threats.
        # Specifically, the only threats it solves are already solved by its Lowinverse.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [1, 1, 0, 1, 1, 0, 0, ],
            ],
            [
                [0, 1, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 0, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        square_to_threats = board.potential_threats_by_square()

        # Lowinverse c4-c5-d4-d5 guarantees that Black will get at least one square
        # out of each of three pairs of squares:
        # 1. The squares in the first column (c4-c5).
        # 2. The squares in the other column (d4-d5).
        # 3. The upper two squares (c5-d5).
        lowinverse_c4_c5_d4_d5 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=1, col=2), lower=Square(row=2, col=2)),  # c4-c5
            second_vertical=Vertical(upper=Square(row=1, col=3), lower=Square(row=2, col=3)),  # d4-d5
        )
        got_lowinverse_solution = solution.from_lowinverse(
            lowinverse=lowinverse_c4_c5_d4_d5,
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(got_lowinverse_solution)

        # Highinverse c4-c5-c6-d4-d5-d6 does not refute any threats that the
        # Lowinverse which is part of it doesn't already refute.
        highinverse_c4_c5_c6_d4_d5_d6 = Highinverse(
            lowinverse=lowinverse_c4_c5_d4_d5,
        )
        got_highinverse_solution = solution.from_highinverse(
            highinverse=highinverse_c4_c5_c6_d4_d5_d6,
            square_to_threats=square_to_threats,
            directly_playable_squares=board.playable_squares(),
        )
        self.assertIsNone(got_highinverse_solution)

    def test_from_highinverse_useless_highinverse_useful_vertical(self):
        # This test verifies that a Highinverse is not converted into a Solution
        # if it doesn't create any new potential threats.
        # Specifically, the only threats it solves are already solved by one of its Verticals.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [1, 1, 1, 0, 0, 0, 0, ],
                [1, 1, 0, 1, 1, 0, 0, ],
            ],
            [
                [0, 1, 0, 0, 1, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        square_to_threats = board.potential_threats_by_square()

        # Lowinverse c4-c5-d4-d5 does not refute any threats that the
        # Verticals which are part of it don't already refute.
        lowinverse_c4_c5_d4_d5 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=1, col=2), lower=Square(row=2, col=2)),  # c4-c5
            second_vertical=Vertical(upper=Square(row=1, col=3), lower=Square(row=2, col=3)),  # d4-d5
        )
        got_lowinverse_solution = solution.from_lowinverse(
            lowinverse=lowinverse_c4_c5_d4_d5,
            square_to_threats=square_to_threats,
        )
        self.assertIsNone(got_lowinverse_solution)

        # Highinverse c4-c5-c6-d4-d5-d6 does not refute any threats that
        # Vertical c4-c5 which is part of it doesn't already refute.
        highinverse_c4_c5_c6_d4_d5_d6 = Highinverse(
            lowinverse=lowinverse_c4_c5_d4_d5,
        )
        got_highinverse_solution = solution.from_highinverse(
            highinverse=highinverse_c4_c5_c6_d4_d5_d6,
            square_to_threats=square_to_threats,
            directly_playable_squares=board.playable_squares(),
        )
        self.assertIsNone(got_highinverse_solution)

    def test_from_baseclaim(self):
        # This board is from Diagram 6.7 of the original paper.
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
        square_to_threats = board.potential_threats_by_square()

        # Baseclaim b1-c1-c2-e1 can be used to refute b1-e4 and c1-f1.
        baseclaim_b1_c1_c2_f1 = Baseclaim(
            first=Square(row=5, col=1),  # b1
            second=Square(row=5, col=2),  # c1
            third=Square(row=5, col=4),  # e1
        )

        got_solution = solution.from_baseclaim(
            baseclaim=baseclaim_b1_c1_c2_f1,
            square_to_threats=square_to_threats,
        )
        want_solution = Solution(
            rule=Rule.Baseclaim,
            squares=frozenset([
                Square(row=5, col=1),  # b1
                Square(row=5, col=2),  # c1
                Square(row=4, col=2),  # c2
                Square(row=5, col=4),  # e1
            ]),
            threats=frozenset([
                Threat(player=0, start=Square(row=5, col=1), end=Square(row=2, col=4)),  # b1-e4
                Threat(player=0, start=Square(row=5, col=2), end=Square(row=5, col=5)),  # c1-f1
                Threat(player=0, start=Square(row=5, col=1), end=Square(row=5, col=4)),  # b1-e1
            ]),
            claimeven_bottom_squares=[
                Square(row=5, col=2),  # c1
            ],
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_before(self):
        # This board is from Diagram 6.9 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        square_to_threats = board.potential_threats_by_square()

        # Before b4-e1+b5+e2 refutes b5-e2.
        before_b4_e1 = Before(
            threat=Threat(player=1, start=Square(row=2, col=1), end=Square(row=5, col=4)),  # Threat b4-e1
            verticals=[
                Vertical(upper=Square(row=4, col=4), lower=Square(row=5, col=4)),  # Vertical e1-e2
            ],
            claimevens=[
                Claimeven(upper=Square(row=2, col=1), lower=Square(row=3, col=1))  # Claimeven b3-b4
            ]
        )

        got_solution = solution.from_before(before_b4_e1, square_to_threats)
        want_solution = Solution(
            rule=Rule.Before,
            squares=frozenset([
                # Empty squares part of the Before group.
                Square(row=2, col=1),  # b4
                Square(row=5, col=4),  # e1
                # Squares part of Claimevens/Verticals not part of the Before group.
                Square(row=3, col=1),  # b3
                Square(row=4, col=4),  # e2
            ]),
            threats=frozenset([
                # Threats that include all successors of empty squares of the Before group.
                Threat(player=0, start=Square(row=1, col=1), end=Square(row=4, col=4)),  # b5-e2
                # Threats that include upper square of Claimeven b3-b4.
                Threat(player=0, start=Square(row=2, col=0), end=Square(row=2, col=3)),  # a4-d4
                Threat(player=0, start=Square(row=2, col=1), end=Square(row=2, col=4)),  # b4-e4
                Threat(player=0, start=Square(row=3, col=0), end=Square(row=0, col=3)),  # a3-d6
                Threat(player=0, start=Square(row=5, col=1), end=Square(row=2, col=1)),  # b1-b4
                Threat(player=0, start=Square(row=4, col=1), end=Square(row=1, col=1)),  # b2-b5
                Threat(player=0, start=Square(row=3, col=1), end=Square(row=0, col=1)),  # b3-b6
                # Threats that include both squares of Vertical e1-e2.
                Threat(player=0, start=Square(row=5, col=4), end=Square(row=2, col=4)),  # e1-e4
            ]),
            claimeven_bottom_squares=[
                Square(row=3, col=1),  # b3
            ],
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_specialbefore(self):
        # This board is from Diagram 6.10 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        square_to_threats = board.potential_threats_by_square()

        # Verticals/Claimevens which are part of the Before.
        vertical_e2_e3 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))  # Vertical e2-e3.
        claimeven_f1_f2 = Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5))  # Claimeven f1-f2.
        claimeven_g1_g2 = Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6))  # Claimeven g1-g2.

        # Before d2-g2.
        before_d2_g2 = Before(
            threat=Threat(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
            verticals=[vertical_e2_e3],
            claimevens=[claimeven_f1_f2, claimeven_g1_g2],
        )
        # Specialbefore d2-g2.
        specialbefore_d2_g2 = Specialbefore(
            before=before_d2_g2,
            internal_directly_playable_square=Square(row=4, col=4),  # e2
            external_directly_playable_square=Square(row=3, col=3),  # d3
        )

        got_solution = solution.from_specialbefore(
            specialbefore=specialbefore_d2_g2,
            square_to_threats=square_to_threats,
        )
        want_solution = Solution(
            rule=Rule.Specialbefore,
            squares=frozenset([
                # Empty squares part of the Specialbefore group.
                Square(row=4, col=4),  # e2. Note that this is the internal directly playable square.
                Square(row=4, col=5),  # f2
                Square(row=4, col=6),  # g2
                # Squares not part of the Specialbefore group but are
                # part of Verticals/Claimevens which are part of the Specialbefore.
                Square(row=3, col=4),  # e3 is the upper Square of Vertical e2-e3.
                Square(row=5, col=5),  # f1 is the lower Square of Claimeven f1-f2.
                Square(row=5, col=6),  # g1 is the lower Square of Claimeven g1-g2.
                # Directly playable square not part of the Specialbefore group.
                Square(row=3, col=3),  # d3
            ]),
            threats=frozenset([
                # Threats that contain the external directly playable square and
                # all successors of empty squares of the Specialbefore.
                Threat(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6)),  # d3-g3
                # Threats that contain the internal directly playable square and
                # external directly playable square of the Specialbefore.
                Threat(player=0, start=Square(row=1, col=1), end=Square(row=4, col=4)),  # b5-e2
                Threat(player=0, start=Square(row=2, col=2), end=Square(row=5, col=5)),  # c4-f1
                # Threats that are refuted by Vertical e2-e3.
                Threat(player=0, start=Square(row=1, col=4), end=Square(row=4, col=4)),  # e2-e5
                # Threats that are refuted by Claimeven f1-f2.
                Threat(player=0, start=Square(row=1, col=5), end=Square(row=4, col=5)),  # f2-f5
                Threat(player=0, start=Square(row=2, col=5), end=Square(row=5, col=5)),  # f1-f4
                Threat(player=0, start=Square(row=2, col=3), end=Square(row=5, col=6)),  # d4-g1
                # Threats that are refuted by Claimeven g1-g2.
                Threat(player=0, start=Square(row=1, col=6), end=Square(row=4, col=6)),  # g2-g5
                Threat(player=0, start=Square(row=2, col=6), end=Square(row=5, col=6)),  # g1-g4
                Threat(player=0, start=Square(row=1, col=3), end=Square(row=4, col=6)),  # d5-g4
            ]),
            claimeven_bottom_squares=[
                Square(row=5, col=5),  # f1 is the lower Square of Claimeven f1-f2.
                Square(row=5, col=6),  # g1 is the lower Square of Claimeven g1-g2.
            ],
        )
        self.assertEqual(want_solution, got_solution)


if __name__ == '__main__':
    unittest.main()
