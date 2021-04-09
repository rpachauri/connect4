import gym
import unittest

import numpy as np

from connect_four.game import Square
from connect_four.problem import Group
from connect_four.evaluation.victor.board import Board

from connect_four.evaluation.victor.rules import Claimeven
from connect_four.evaluation.victor.rules import Vertical
from connect_four.evaluation.victor.rules import Before
from connect_four.evaluation.victor.rules import find_all_befores
from connect_four.evaluation.victor.rules.before import add_before_variations
from connect_four.evaluation.victor.rules.before import empty_squares_of_before_group

from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.problem.problem_manager import ProblemManager


class TestBefore(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_before(self):
        self.env.state = np.array([
            [
                [0, 0, 1, 0, 0, 0, 1, ],
                [1, 1, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [1, 1, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [1, 1, 0, 1, 1, 0, 1, ],
            ],
            [
                [1, 1, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [1, 1, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [1, 1, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        # With White to move, every Before group must belong to Black.
        black_groups = board.potential_groups(1)
        got_befores = find_all_befores(board, black_groups)

        group_4_3_to_4_6 = Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6))
        group_2_3_to_2_6 = Group(player=1, start=Square(row=2, col=3), end=Square(row=2, col=6))
        group_1_3_to_4_6 = Group(player=1, start=Square(row=1, col=3), end=Square(row=4, col=6))
        group_0_5_to_3_5 = Group(player=1, start=Square(row=0, col=5), end=Square(row=3, col=5))
        group_1_5_to_4_5 = Group(player=1, start=Square(row=1, col=5), end=Square(row=4, col=5))
        group_2_5_to_5_5 = Group(player=1, start=Square(row=2, col=5), end=Square(row=5, col=5))
        want_groups = {
            group_4_3_to_4_6,
            group_2_3_to_2_6,
            group_1_3_to_4_6,
            group_0_5_to_3_5,
            group_1_5_to_4_5,
            group_2_5_to_5_5,
        }
        self.assertEqual(want_groups, black_groups)

        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        vertical_1_5 = Vertical(upper=Square(row=1, col=5), lower=Square(row=2, col=5))
        vertical_2_5 = Vertical(upper=Square(row=2, col=5), lower=Square(row=3, col=5))

        want_befores = {
            Before(group=group_4_3_to_4_6, verticals=[vertical_3_5], claimevens=[]),
            Before(group=group_2_3_to_2_6, verticals=[vertical_1_5], claimevens=[]),
            # The Before below is excluded because it doesn't have any verticals. This makes it an Aftereven.
            # claimeven_3_5 = Claimeven(upper=Square(row=2, col=5), lower=Square(row=3, col=5))
            # Before(group=group_2_3_to_2_6, verticals=[], claimevens=[claimeven_3_5]),
            Before(group=group_1_3_to_4_6, verticals=[vertical_3_5], claimevens=[]),
            Before(group=group_1_3_to_4_6, verticals=[vertical_2_5], claimevens=[]),
        }
        self.assertEqual(want_befores, got_befores)

    def test_add_before_variations_diagram_6_8(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        group_4_3_to_4_6 = Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6))

        befores = set()
        add_before_variations(board=board,
                              befores=befores,
                              group=group_4_3_to_4_6,
                              empty_squares=[Square(row=4, col=5)],
                              verticals=[],
                              claimevens=[])
        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        want_befores = {
            Before(group=group_4_3_to_4_6, verticals=[vertical_3_5], claimevens=[]),
        }
        self.assertEqual(want_befores, befores)

    def test_add_before_variations_diagram_6_9(self):
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
        group_2_1_to_5_4 = Group(player=1, start=Square(row=2, col=1), end=Square(row=5, col=4))

        befores = set()
        add_before_variations(board=board,
                              befores=befores,
                              group=group_2_1_to_5_4,
                              empty_squares=[Square(row=2, col=1), Square(row=5, col=4)],
                              verticals=[],
                              claimevens=[])
        vertical_1_1 = Vertical(upper=Square(row=1, col=1), lower=Square(row=2, col=1))
        claimeven_2_1 = Claimeven(upper=Square(row=2, col=1), lower=Square(row=3, col=1))
        vertical_4_4 = Vertical(upper=Square(row=4, col=4), lower=Square(row=5, col=4))
        want_befores = {
            Before(group=group_2_1_to_5_4, verticals=[vertical_1_1, vertical_4_4], claimevens=[]),
            Before(group=group_2_1_to_5_4, verticals=[vertical_4_4], claimevens=[claimeven_2_1]),
        }
        self.assertEqual(want_befores, befores)

    def test_add_before_variations_diagram_6_10(self):
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
        group_4_3_to_4_6 = Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6))

        befores = set()
        add_before_variations(board=board,
                              befores=befores,
                              group=group_4_3_to_4_6,
                              empty_squares=[Square(row=4, col=4), Square(row=4, col=5), Square(row=4, col=6)],
                              verticals=[],
                              claimevens=[])
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))
        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        claimeven_4_5 = Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5))
        vertical_3_6 = Vertical(upper=Square(row=3, col=6), lower=Square(row=4, col=6))
        claimeven_4_6 = Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6))
        want_befores = {
            Before(group=group_4_3_to_4_6, verticals=[vertical_3_4, vertical_3_5, vertical_3_6], claimevens=[]),
            Before(group=group_4_3_to_4_6, verticals=[vertical_3_4, vertical_3_5], claimevens=[claimeven_4_6]),
            Before(group=group_4_3_to_4_6, verticals=[vertical_3_4, vertical_3_6], claimevens=[claimeven_4_5]),
            Before(group=group_4_3_to_4_6, verticals=[vertical_3_4], claimevens=[claimeven_4_5, claimeven_4_6]),
        }
        self.assertEqual(want_befores, befores)

        want_empty_squares = frozenset([Square(row=4, col=4), Square(row=4, col=5), Square(row=4, col=6)])
        for b in befores:
            self.assertSetEqual(want_empty_squares, b.empty_squares_of_before_group())

    def test_empty_squares_of_before_group_diagram_6_10(self):
        # Note that this tests the function empty_squares_of_before_group.
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
        group_4_3_to_4_6 = Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)
                                 )
        want_empty_squares = [Square(row=4, col=4), Square(row=4, col=5), Square(row=4, col=6)]
        got_empty_squares = empty_squares_of_before_group(board=board, group=group_4_3_to_4_6)
        self.assertCountEqual(want_empty_squares, got_empty_squares)

    def test_empty_squares_of_before_group_top_row_taken(self):
        # This test case validates that a Before group is still valid even when it contains
        # a Square in the top row as long as that square is not empty.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        group_a3_d6 = Group(player=1, start=Square(row=3, col=0), end=Square(row=0, col=3))  # a3-d6

        want_empty_squares = [
            Square(row=3, col=0),  # a3
            Square(row=2, col=1),  # b4
            Square(row=1, col=2),  # c5
        ]
        got_empty_squares = empty_squares_of_before_group(board=board, group=group_a3_d6)
        self.assertCountEqual(want_empty_squares, got_empty_squares)

    def test_empty_squares_of_before_group_top_row_empty(self):
        # This test case validates that if a Group contains an empty square in the top row, no Befores use it.
        # However, if that square is taken by a player, that player can use it in some Befores.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        group_a3_d6 = Group(player=1, start=Square(row=3, col=0), end=Square(row=0, col=3))  # a3-d6

        # Since d6 is an empty square in the top row, no Before groups containing d6 can be formed.
        got_befores = find_all_befores(board=board, opponent_groups={group_a3_d6})
        # Assert that got_befores is empty.
        self.assertFalse(got_befores)

        # Note that this isn't an ideal use of Board because a Board instance should ideally be immutable.
        # White plays d5.
        board.state[0][1][3] = 1
        # Black plays d6.
        board.state[1][0][3] = 1

        # Now that d6 has been taken by White, White can use it in some Before groups.
        got_befores = find_all_befores(board=board, opponent_groups={group_a3_d6})
        # Assert that got_befores is not empty.
        self.assertTrue(got_befores)

    def test_find_problems_solved(self):
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
        pm = ProblemManager(env_variables=self.env.env_variables, num_to_connect=4)

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

        want_problems_solved = {
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
        }
        got_problems_solved = before_b4_e1.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_problems_solved, got_problems_solved)


if __name__ == '__main__':
    unittest.main()
