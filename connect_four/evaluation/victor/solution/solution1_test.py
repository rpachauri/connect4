import gym
import unittest

import numpy as np

from connect_four.evaluation.victor.rules.highinverse import HighinverseColumn
from connect_four.evaluation.victor.rules.threat_combination import ThreatCombinationType
from connect_four.game import Square
from connect_four.problem import Group
from connect_four.evaluation.board import Board

from connect_four.evaluation.victor.rules import Claimeven, ThreatCombination
from connect_four.evaluation.victor.rules import Baseinverse
from connect_four.evaluation.victor.rules import Vertical
from connect_four.evaluation.victor.rules import Aftereven
from connect_four.evaluation.victor.rules import Lowinverse
from connect_four.evaluation.victor.rules import Highinverse
from connect_four.evaluation.victor.rules import Baseclaim
from connect_four.evaluation.victor.rules import Before
from connect_four.evaluation.victor.rules import Specialbefore

from connect_four.evaluation.victor.solution import Solution
from connect_four.evaluation.victor.solution import solution1

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestSolution1(unittest.TestCase):
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
        square_to_groups = board.potential_groups_by_square()

        # We're using the Claimeven with the upper square being e4.
        # In the example from the original paper, this refutes the groups in (4):
        # d3-g6, c2-f5, b1-e4, e3-e6
        claimeven_2_4 = Claimeven(upper=Square(row=2, col=4), lower=Square(row=3, col=4))

        got_solution = solution1.from_claimeven(claimeven_2_4, square_to_groups)
        want_solution = Solution(
            squares=frozenset([claimeven_2_4.upper, claimeven_2_4.lower]),
            groups=frozenset([
                Group(player=0, start=Square(row=3, col=3), end=Square(row=0, col=6)),  # d3-g6
                Group(player=0, start=Square(row=4, col=2), end=Square(row=1, col=5)),  # c2-f5
                Group(player=0, start=Square(row=5, col=1), end=Square(row=2, col=4)),  # b1-e4
                Group(player=0, start=Square(row=3, col=4), end=Square(row=0, col=4)),  # e3-d6
            ]),
            claimeven_bottom_squares=[claimeven_2_4.lower],
            rule_instance=claimeven_2_4,
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
        square_to_groups = board.potential_groups_by_square()

        # The Baseinverse a1-b1 solves a1-d1.
        baseinverse_a1_b1 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=5, col=1))

        got_solution = solution1.from_baseinverse(baseinverse_a1_b1, square_to_groups)
        want_solution = Solution(
            squares=frozenset(baseinverse_a1_b1.squares),
            groups=frozenset([
                Group(player=0, start=Square(row=5, col=0), end=Square(row=5, col=3)),  # a1-d1
            ]),
            rule_instance=baseinverse_a1_b1,
        )
        self.assertEqual(want_solution, got_solution)

        # As stated in the original paper, the Baseinverse a1-c4 is possible but useless.
        # Thus, it should not be converted into a Solution.
        baseinverse_a1_c4 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=2, col=2))
        self.assertIsNone(solution1.from_baseinverse(baseinverse_a1_c4, square_to_groups))

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
        square_to_groups = board.potential_groups_by_square()

        # The Vertical e4-e5 solves e2-e5 and e3-e6.
        vertical_e4_e5 = Vertical(upper=Square(row=2, col=4), lower=Square(row=1, col=4))

        got_solution = solution1.from_vertical(vertical_e4_e5, square_to_groups)
        want_solution = Solution(
            squares=frozenset([vertical_e4_e5.upper, vertical_e4_e5.lower]),
            groups=frozenset([
                Group(player=0, start=Square(row=4, col=4), end=Square(row=1, col=4)),  # e2-e5
                Group(player=0, start=Square(row=3, col=4), end=Square(row=0, col=4)),  # e3-e6
            ]),
            rule_instance=vertical_e4_e5,
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
        square_to_groups = board.potential_groups_by_square()

        # The Aftereven d2-g2 solves all groups which need a square in both the f and g column.
        aftereven_d2_g2 = Aftereven(
            group=Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
            claimevens=[
                Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5)),  # Claimeven f1-f2
                Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6)),  # Claimeven g1-g2
            ],
        )

        got_solution = solution1.from_aftereven(aftereven_d2_g2, square_to_groups)
        want_solution = Solution(
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
            groups=frozenset([
                # New groups from Aftereven.
                Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6)),  # d3-g3
                Group(player=0, start=Square(row=1, col=3), end=Square(row=1, col=6)),  # d5-g5
                Group(player=0, start=Square(row=0, col=3), end=Square(row=0, col=6)),  # d6-g6
                Group(player=0, start=Square(row=0, col=3), end=Square(row=3, col=6)),  # d0-g3
                # groups refuted by Claimeven f1-f2.
                Group(player=0, start=Square(row=2, col=5), end=Square(row=5, col=5)),  # f1-f4
                Group(player=0, start=Square(row=1, col=5), end=Square(row=4, col=5)),  # f2-f5
                # groups refuted by Claimeven g1-g2.
                Group(player=0, start=Square(row=2, col=6), end=Square(row=5, col=6)),  # g1-g4
                Group(player=0, start=Square(row=1, col=6), end=Square(row=4, col=6)),  # g2-g5
            ]),
            claimeven_bottom_squares=[
                # Lower squares of Claimevens.
                Square(row=5, col=5),
                Square(row=5, col=6),
            ],
            rule_instance=aftereven_d2_g2,
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
        square_to_groups = board.potential_groups_by_square()

        # Lowinverse c2-c3-d2-d3 guarantees that Black will get at least one square
        # out of each of three pairs of squares:
        # 1. The squares in the first column (c2-c3).
        # 2. The squares in the other column (d2-d3).
        # 3. The upper two squares (c3-d3).
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2)),  # c2-c3
            second_vertical=Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3)),  # d2-d3
        )

        got_solution = solution1.from_lowinverse(lowinverse_c2_c3_d2_d3, square_to_groups)
        want_solution = Solution(
            squares=frozenset([
                Square(row=3, col=2),
                Square(row=4, col=2),
                Square(row=3, col=3),
                Square(row=4, col=3),
            ]),
            groups=frozenset([
                # groups which contain both upper squares of the Verticals.
                Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
                Group(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
                Group(player=0, start=Square(row=3, col=2), end=Square(row=3, col=5)),  # c3-f3
                # groups refuted by Vertical c2-c3.
                Group(player=0, start=Square(row=1, col=2), end=Square(row=4, col=2)),  # c2-c5
                # Note that c1-c4 does not need to be refuted because Black already occupies c1.
                # groups refuted by Vertical d2-d3.
                Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=3)),  # d2-d5
                Group(player=0, start=Square(row=2, col=3), end=Square(row=5, col=3)),  # d1-d4
            ]),
            rule_instance=lowinverse_c2_c3_d2_d3,
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_highinverse_using_highinverse_columns(self):
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
        square_to_groups = board.potential_groups_by_square()

        # Highinverse c2-c3-c4-e2-e3-e4 guarantees at least one square
        # out of each pairs of squares:
        # 1. The upper two squares in the first column (c3-c4).
        # 2. The upper two squares in the second column (e3-e4).
        # 3. The middle squares from both columns (c3-e3).
        # 4. The upper squares from both columns (c4-e4).
        # 5. The lower square in the first column (since it's directly playable) and
        #    the upper square in the second column (c2-e4).
        # 6. The lower square in the second column (since it's directly playable) and
        #    the upper square in the first column (c4-e2).
        highinverse_c2_c3_c4_e2_e3_e4 = Highinverse(
            columns={
                HighinverseColumn(
                    upper=Square(row=2, col=2),  # c4
                    middle=Square(row=3, col=2),  # c3
                    lower=Square(row=4, col=2),  # c2
                    directly_playable=True,
                ),
                HighinverseColumn(
                    upper=Square(row=2, col=4),  # e4
                    middle=Square(row=3, col=4),  # e3
                    lower=Square(row=4, col=4),  # e2
                    directly_playable=True,
                ),
            }
        )

        want_solution = Solution(
            squares=frozenset([
                Square(row=2, col=2),  # c4
                Square(row=3, col=2),  # c3
                Square(row=4, col=2),  # c2
                Square(row=2, col=4),  # e4
                Square(row=3, col=4),  # e3
                Square(row=4, col=4),  # e2
            ]),
            groups=frozenset({
                # Groups solved by c3-c4.
                Group(player=0, start=Square(row=1, col=2), end=Square(row=4, col=2)),  # c2-c5
                Group(player=0, start=Square(row=0, col=2), end=Square(row=3, col=2)),  # c3-c6
                # Groups solved by e3-e4.
                Group(player=0, start=Square(row=2, col=4), end=Square(row=5, col=4)),  # e1-e4
                Group(player=0, start=Square(row=1, col=4), end=Square(row=4, col=4)),  # e2-e5
                Group(player=0, start=Square(row=0, col=4), end=Square(row=3, col=4)),  # e3-e6
                # Groups solved by c3-e3.
                Group(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
                Group(player=0, start=Square(row=3, col=2), end=Square(row=3, col=5)),  # c3-f3
                # Groups solved by c4-e4.
                Group(player=0, start=Square(row=2, col=1), end=Square(row=2, col=4)),  # b4-e4
                Group(player=0, start=Square(row=2, col=2), end=Square(row=2, col=5)),  # c4-f4
                # Groups solved by c2-e4.
                Group(player=0, start=Square(row=5, col=1), end=Square(row=2, col=4)),  # b1-e4
                Group(player=0, start=Square(row=4, col=2), end=Square(row=1, col=5)),  # c2-f5
                # Groups solved by c4-e2.
                Group(player=0, start=Square(row=1, col=1), end=Square(row=4, col=4)),  # b5-e2
                Group(player=0, start=Square(row=2, col=2), end=Square(row=5, col=5)),  # c4-f1
            }),
            rule_instance=highinverse_c2_c3_c4_e2_e3_e4,
        )
        got_solution = solution1.from_highinverse(
            highinverse=highinverse_c2_c3_c4_e2_e3_e4,
            square_to_groups=square_to_groups,
        )
        self.assertEqual(want_solution, got_solution)

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
        square_to_groups = board.potential_groups_by_square()

        # Baseclaim b1-c1-c2-e1 can be used to refute b1-e4 and c1-f1.
        baseclaim_b1_c1_c2_f1 = Baseclaim(
            first=Square(row=5, col=1),  # b1
            second=Square(row=5, col=2),  # c1
            third=Square(row=5, col=4),  # e1
        )

        got_solution = solution1.from_baseclaim(
            baseclaim=baseclaim_b1_c1_c2_f1,
            square_to_groups=square_to_groups,
        )
        want_solution = Solution(
            squares=frozenset([
                Square(row=5, col=1),  # b1
                Square(row=5, col=2),  # c1
                Square(row=4, col=2),  # c2
                Square(row=5, col=4),  # e1
            ]),
            groups=frozenset([
                Group(player=0, start=Square(row=5, col=1), end=Square(row=2, col=4)),  # b1-e4
                Group(player=0, start=Square(row=5, col=2), end=Square(row=5, col=5)),  # c1-f1
                Group(player=0, start=Square(row=5, col=1), end=Square(row=5, col=4)),  # b1-e1
            ]),
            claimeven_bottom_squares=[
                Square(row=5, col=2),  # c1
            ],
            rule_instance=baseclaim_b1_c1_c2_f1,
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
        square_to_groups = board.potential_groups_by_square()

        # Before b4-e1+b5+e2 refutes b5-e2.
        before_b4_e1 = Before(
            group=Group(player=1, start=Square(row=2, col=1), end=Square(row=5, col=4)),  # Group b4-e1
            verticals=[
                Vertical(upper=Square(row=4, col=4), lower=Square(row=5, col=4)),  # Vertical e1-e2
            ],
            claimevens=[
                Claimeven(upper=Square(row=2, col=1), lower=Square(row=3, col=1))  # Claimeven b3-b4
            ]
        )

        got_solution = solution1.from_before(before_b4_e1, square_to_groups)
        want_solution = Solution(
            squares=frozenset([
                # Empty squares part of the Before group.
                Square(row=2, col=1),  # b4
                Square(row=5, col=4),  # e1
                # Squares part of Claimevens/Verticals not part of the Before group.
                Square(row=3, col=1),  # b3
                Square(row=4, col=4),  # e2
            ]),
            groups=frozenset([
                # groups that include all successors of empty squares of the Before group.
                Group(player=0, start=Square(row=1, col=1), end=Square(row=4, col=4)),  # b5-e2
                # groups that include upper square of Claimeven b3-b4.
                Group(player=0, start=Square(row=2, col=0), end=Square(row=2, col=3)),  # a4-d4
                Group(player=0, start=Square(row=2, col=1), end=Square(row=2, col=4)),  # b4-e4
                Group(player=0, start=Square(row=3, col=0), end=Square(row=0, col=3)),  # a3-d6
                Group(player=0, start=Square(row=5, col=1), end=Square(row=2, col=1)),  # b1-b4
                Group(player=0, start=Square(row=4, col=1), end=Square(row=1, col=1)),  # b2-b5
                Group(player=0, start=Square(row=3, col=1), end=Square(row=0, col=1)),  # b3-b6
                # groups that include both squares of Vertical e1-e2.
                Group(player=0, start=Square(row=5, col=4), end=Square(row=2, col=4)),  # e1-e4
            ]),
            claimeven_bottom_squares=[
                Square(row=3, col=1),  # b3
            ],
            rule_instance=before_b4_e1,
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
        square_to_groups = board.potential_groups_by_square()

        # Verticals/Claimevens which are part of the Before.
        vertical_e2_e3 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))  # Vertical e2-e3.
        claimeven_f1_f2 = Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5))  # Claimeven f1-f2.
        claimeven_g1_g2 = Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6))  # Claimeven g1-g2.

        # Before d2-g2.
        before_d2_g2 = Before(
            group=Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
            verticals=[vertical_e2_e3],
            claimevens=[claimeven_f1_f2, claimeven_g1_g2],
        )
        # Specialbefore d2-g2+e2+d3.
        specialbefore_d2_g2 = Specialbefore(
            before=before_d2_g2,
            internal_directly_playable_square=Square(row=4, col=4),  # e2
            external_directly_playable_square=Square(row=3, col=3),  # d3
        )

        got_solution = solution1.from_specialbefore(
            specialbefore=specialbefore_d2_g2,
            square_to_groups=square_to_groups,
        )
        want_solution = Solution(
            squares=frozenset([
                # Empty squares part of the Specialbefore group.
                Square(row=4, col=4),  # e2. Note that this is the internal directly playable square.
                Square(row=4, col=5),  # f2
                Square(row=4, col=6),  # g2
                # Squares not part of the Specialbefore group but are
                # part of Verticals/Claimevens which are part of the Specialbefore.
                # Square(row=3, col=4),  # e3 is the upper Square of Vertical e2-e3 and does not get used.
                Square(row=5, col=5),  # f1 is the lower Square of Claimeven f1-f2.
                Square(row=5, col=6),  # g1 is the lower Square of Claimeven g1-g2.
                # Directly playable square not part of the Specialbefore group.
                Square(row=3, col=3),  # d3
            ]),
            groups=frozenset([
                # groups that contain the external directly playable square and
                # all successors of empty squares of the Specialbefore.
                Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6)),  # d3-g3
                # groups that contain the internal directly playable square and
                # external directly playable square of the Specialbefore.
                Group(player=0, start=Square(row=1, col=1), end=Square(row=4, col=4)),  # b5-e2
                Group(player=0, start=Square(row=2, col=2), end=Square(row=5, col=5)),  # c4-f1
                # Note that Vertical e2-e3 does not get used.
                # Group(player=0, start=Square(row=1, col=4), end=Square(row=4, col=4)),  # e2-e5
                # groups that are refuted by Claimeven f1-f2.
                Group(player=0, start=Square(row=1, col=5), end=Square(row=4, col=5)),  # f2-f5
                Group(player=0, start=Square(row=2, col=5), end=Square(row=5, col=5)),  # f1-f4
                Group(player=0, start=Square(row=2, col=3), end=Square(row=5, col=6)),  # d4-g1
                # groups that are refuted by Claimeven g1-g2.
                Group(player=0, start=Square(row=1, col=6), end=Square(row=4, col=6)),  # g2-g5
                Group(player=0, start=Square(row=2, col=6), end=Square(row=5, col=6)),  # g1-g4
                Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=6)),  # d5-g4
            ]),
            claimeven_bottom_squares=[
                Square(row=5, col=5),  # f1 is the lower Square of Claimeven f1-f2.
                Square(row=5, col=6),  # g1 is the lower Square of Claimeven g1-g2.
            ],
            rule_instance=specialbefore_d2_g2,
        )
        self.assertEqual(want_solution, got_solution)

    def test_useless_specialbefore(self):
        # An empty board.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        square_to_groups = board.potential_groups_by_square()

        # Verticals/Claimevens which are part of the Before.
        vertical_b4_b5 = Vertical(upper=Square(row=1, col=1), lower=Square(row=2, col=1))
        vertical_c2_c3 = Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2))
        claimeven_d1_d2 = Claimeven(upper=Square(row=4, col=3), lower=Square(row=5, col=3))
        vertical_e1_e2 = Vertical(upper=Square(row=4, col=4), lower=Square(row=5, col=4))
        # Before d2-g2.
        before_d2_g2 = Before(
            group=Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
            verticals=[vertical_b4_b5, vertical_c2_c3, vertical_e1_e2],
            claimevens=[claimeven_d1_d2],
        )
        # Specialbefore d2-g2+e1+d1.
        specialbefore_d2_g2 = Specialbefore(
            before=before_d2_g2,
            internal_directly_playable_square=Square(row=5, col=4),  # e1
            external_directly_playable_square=Square(row=5, col=3),  # d1
        )
        # Note that there are no groups that contain b5-e2 and d1 because that is not possible.
        # Thus, this Specialbefore is useless.

        got_solution = solution1.from_specialbefore(
            specialbefore=specialbefore_d2_g2,
            square_to_groups=square_to_groups,
        )
        self.assertIsNone(got_solution)

    def test_no_odd_squares_in_crossing_column(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 1, 0, ],
                [0, 0, 0, 1, 0, 1, 0, ],
            ],
            [
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1  # Black to move.
        board = Board(self.env.env_variables)
        square_to_groups = board.potential_groups_by_square()

        even_group = Group(player=0, start=Square(row=3, col=3), end=Square(row=0, col=6))  # d3-g6
        odd_group = Group(player=0, start=Square(row=1, col=3), end=Square(row=1, col=6))  # d5-g5
        threat_combination_d3g6_d5g5 = ThreatCombination(
            even_group=even_group,
            odd_group=odd_group,
            shared_square=Square(row=1, col=5),  # f5
            even_square=Square(row=0, col=6),  # g6
            odd_square=Square(row=1, col=6),  # g5
            directly_playable_square_shared_col=Square(row=3, col=5),  # f3
            directly_playable_square_stacked_col=Square(row=5, col=6),  # g1
            threat_combination_type=ThreatCombinationType.EvenAboveOdd,
        )
        got_solution = solution1.from_even_above_odd_threat_combination(
            threat_combination=threat_combination_d3g6_d5g5,
            square_to_groups=square_to_groups,
        )
        group_c1_f4 = Group(player=1, start=Square(row=5, col=2), end=Square(row=2, col=5))  # c1-f4
        self.assertNotIn(group_c1_f4, got_solution.groups)

    def test_vertical_groups_in_stacked_column(self):
        # This test case is based on Diagram 8.3.
        # Black is to move and White has a ThreatCombination at d1-g4 and d3-g3.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 1, ],
            ],
            [
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1  # Black to move.
        board = Board(self.env.env_variables)
        square_to_groups = board.potential_groups_by_square()

        even_group = Group(player=0, start=Square(row=5, col=3), end=Square(row=2, col=6))  # d1-g4
        odd_group = Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6))  # d3-g3
        threat_combination_d1g4_d3g3 = ThreatCombination(
            even_group=even_group,
            odd_group=odd_group,
            shared_square=Square(row=3, col=5),  # f3
            even_square=Square(row=2, col=6),  # g4
            odd_square=Square(row=3, col=6),  # g3
            directly_playable_square_shared_col=Square(row=5, col=5),  # f1
            directly_playable_square_stacked_col=Square(row=4, col=6),  # g2
            threat_combination_type=ThreatCombinationType.EvenAboveOdd,
        )
        got_solution = solution1.from_even_above_odd_threat_combination(
            threat_combination=threat_combination_d1g4_d3g3,
            square_to_groups=square_to_groups,
        )
        # As stated at the end of Section 8.3 of the original paper, White "gets one out of every two squares
        # in the g-column starting from the first playable square up to and including g4". This means that
        # White can refute g3-g6.
        group_g3_g6 = Group(player=1, start=Square(row=3, col=6), end=Square(row=0, col=6))  # g3-g6
        self.assertIn(group_g3_g6, got_solution.groups)


if __name__ == '__main__':
    unittest.main()
