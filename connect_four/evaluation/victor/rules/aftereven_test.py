import gym
import unittest

import numpy as np

from connect_four.game import Square
from connect_four.problem import Group
from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.rules import Claimeven
from connect_four.evaluation.victor.rules import find_all_claimevens
from connect_four.evaluation.victor.rules import Aftereven
from connect_four.evaluation.victor.rules import find_all_afterevens

from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.problem.problem_manager import ProblemManager


class TestAftereven(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_aftereven1(self):
        # This test case is based on Diagram 6.4.
        # Extra tokens have been added to reduce the number of possible Aftereven instances.
        self.env.state = np.array([
            [
                [1, 0, 0, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [1, 0, 1, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [1, 0, 0, 0, 0, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 1, 0, 1, 0, 0, ],
                [1, 0, 1, 0, 1, 0, 1, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [1, 0, 0, 0, 0, 0, 1, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [1, 0, 0, 0, 1, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)
        black_groups = board.potential_groups(1)
        got_afterevens = find_all_afterevens(
            board=board,
            claimevens=find_all_claimevens(board),
            opponent_groups=black_groups,
        )

        want_afterevens = {
            Aftereven(
                group=Group(player=1, start=Square(row=4, col=1), end=Square(row=4, col=4)),  # b2-e2
                claimevens=frozenset([Claimeven(upper=Square(row=4, col=1), lower=Square(row=5, col=1))]),
            ),
            Aftereven(
                group=Group(player=1, start=Square(row=4, col=2), end=Square(row=4, col=5)),  # c2-f2
                claimevens=frozenset([Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5))]),
            ),
        }
        self.assertEqual(want_afterevens, got_afterevens)

    def test_aftereven2(self):
        # This test case is based on Diagram 6.5.
        # Extra tokens have been added to reduce the number of possible Aftereven instances.
        self.env.state = np.array([
            [
                [1, 0, 1, 0, 0, 0, 0, ],
                [1, 0, 0, 1, 0, 0, 0, ],
                [1, 1, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 1, 1, 0, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 1, 0, 1, 0, 0, 0, ],
                [0, 1, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [1, 1, 0, 0, 0, 0, 0, ],
                [1, 0, 0, 1, 1, 0, 0, ],
                [1, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        black_groups = board.potential_groups(1)
        got_afterevens = find_all_afterevens(
            board=board,
            claimevens=find_all_claimevens(board),
            opponent_groups=black_groups,
        )

        want_afterevens = {
            Aftereven(
                group=Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
                claimevens=frozenset([
                    Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5)),
                    Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6)),
                ]),
            ),
            Aftereven(
                group=Group(player=1, start=Square(row=2, col=3), end=Square(row=2, col=6)),  # d4-g4
                claimevens=frozenset([
                    Claimeven(upper=Square(row=2, col=5), lower=Square(row=3, col=5)),
                    Claimeven(upper=Square(row=2, col=6), lower=Square(row=3, col=6)),
                ]),
            ),
            Aftereven(
                group=Group(player=1, start=Square(row=2, col=2), end=Square(row=2, col=5)),  # c4-f4
                claimevens=frozenset([
                    Claimeven(upper=Square(row=2, col=5), lower=Square(row=3, col=5)),
                ]),
            ),
        }
        self.assertEqual(want_afterevens, got_afterevens)

    def test_empty_squares_of_aftereven_group_top_row_empty(self):
        # This test case validates that if a Group contains an empty square in the top row, no Afterevens use it.
        # However, if that square is taken by a player, that player can use it in some Afterevens.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [1, 0, 1, 0, 0, 0, 0, ],
                [1, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [1, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1
        board = Board(self.env.env_variables)
        group_a3_d6 = Group(player=1, start=Square(row=3, col=0), end=Square(row=0, col=3))  # a3-d6

        # Since d6 is an empty square in the top row, no Aftereven groups containing d6 can be formed.
        got_afterevens = find_all_afterevens(
            board=board,
            claimevens=find_all_claimevens(board=board),
            opponent_groups={group_a3_d6},
        )
        # Assert that got_afterevens is empty.
        self.assertFalse(got_afterevens)

        # Note that this isn't an ideal use of Board because a Board instance should ideally be immutable.
        # White plays d5.
        board.state[0][1][3] = 1
        # Black plays d6.
        board.state[1][0][3] = 1

        # Now that d6 has been taken by White, White can use it in some Aftereven groups.
        got_afterevens = find_all_afterevens(
            board=board,
            claimevens=find_all_claimevens(board=board),
            opponent_groups={group_a3_d6},
        )
        # Assert that got_afterevens is not empty.
        self.assertTrue(got_afterevens)

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
        pm = ProblemManager(env_variables=self.env.env_variables, num_to_connect=4)

        # The Aftereven d2-g2 solves all groups which need a square in both the f and g column.
        aftereven_d2_g2 = Aftereven(
            group=Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
            claimevens=[
                Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5)),  # Claimeven f1-f2
                Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6)),  # Claimeven g1-g2
            ],
        )

        want_problems_solved = {
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
        }
        got_problems_solved = aftereven_d2_g2.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_problems_solved, got_problems_solved)


if __name__ == '__main__':
    unittest.main()
