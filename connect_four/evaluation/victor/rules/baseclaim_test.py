import gym
import unittest

import numpy as np

from connect_four.evaluation.victor.rules.baseclaim import BaseclaimManager
from connect_four.game import Square
from connect_four.evaluation.victor.board import Board

from connect_four.evaluation.victor.rules import Baseclaim
from connect_four.evaluation.victor.rules import find_all_baseclaims

from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.problem import Group
from connect_four.problem import ConnectFourGroupManager


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
        square_5_4 = Square(row=5, col=4)
        square_4_5 = Square(row=4, col=5)
        square_4_6 = Square(row=4, col=6)

        want_baseclaims = {
            ## Baseclaims where square_5_1 is the second square.
            # Baseclaims where square_4_0 is the first square.
            Baseclaim(first=square_4_0, second=square_5_1, third=square_5_2),
            Baseclaim(first=square_4_0, second=square_5_1, third=square_5_4),
            ## Baseclaims where square_5_2 is the second square.
            # Baseclaims where square_4_0 is the first square.
            Baseclaim(first=square_4_0, second=square_5_2, third=square_5_1),
            Baseclaim(first=square_4_0, second=square_5_2, third=square_5_4),
            # Baseclaims where square_5_1 is the first square.
            Baseclaim(first=square_5_1, second=square_5_2, third=square_5_4),
            # Baseclaims where square_4_5 is the first square.
            Baseclaim(first=square_4_5, second=square_5_2, third=square_5_1),
            Baseclaim(first=square_4_5, second=square_5_2, third=square_5_4),
            ## Baseclaims where square_5_4 is the second square.
            # Baseclaims where square_4_5 is the first square.
            Baseclaim(first=square_4_5, second=square_5_4, third=square_5_1),
            Baseclaim(first=square_4_5, second=square_5_4, third=square_5_2),
            # Baseclaims where square_4_6 is the first square.
            Baseclaim(first=square_4_6, second=square_5_4, third=square_5_1),
            Baseclaim(first=square_4_6, second=square_5_4, third=square_5_2),
        }
        self.assertEqual(want_baseclaims, got_baseclaims)

    def test_baseclaim_manager_initialization(self):
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
        bm = BaseclaimManager(board=board)
        got_baseclaims = bm.baseclaims

        # Directly playable squares.
        square_4_0 = Square(row=4, col=0)
        square_5_1 = Square(row=5, col=1)
        square_5_2 = Square(row=5, col=2)
        square_5_4 = Square(row=5, col=4)
        square_4_5 = Square(row=4, col=5)
        square_4_6 = Square(row=4, col=6)

        want_baseclaims = {
            ## Baseclaims where square_5_1 is the second square.
            # Baseclaims where square_4_0 is the first square.
            Baseclaim(first=square_4_0, second=square_5_1, third=square_5_2),
            Baseclaim(first=square_4_0, second=square_5_1, third=square_5_4),
            ## Baseclaims where square_5_2 is the second square.
            # Baseclaims where square_4_0 is the first square.
            Baseclaim(first=square_4_0, second=square_5_2, third=square_5_1),
            Baseclaim(first=square_4_0, second=square_5_2, third=square_5_4),
            # Baseclaims where square_5_1 is the first square.
            Baseclaim(first=square_5_1, second=square_5_2, third=square_5_4),
            # Baseclaims where square_4_5 is the first square.
            Baseclaim(first=square_4_5, second=square_5_2, third=square_5_1),
            Baseclaim(first=square_4_5, second=square_5_2, third=square_5_4),
            ## Baseclaims where square_5_4 is the second square.
            # Baseclaims where square_4_5 is the first square.
            Baseclaim(first=square_4_5, second=square_5_4, third=square_5_1),
            Baseclaim(first=square_4_5, second=square_5_4, third=square_5_2),
            # Baseclaims where square_4_6 is the first square.
            Baseclaim(first=square_4_6, second=square_5_4, third=square_5_1),
            Baseclaim(first=square_4_6, second=square_5_4, third=square_5_2),
        }
        self.assertEqual(want_baseclaims, got_baseclaims)

    def test_baseclaims_given_first_and_third_square(self):
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

        # Directly playable squares.
        square_4_0 = Square(row=4, col=0)
        square_5_1 = Square(row=5, col=1)
        square_5_2 = Square(row=5, col=2)
        square_5_4 = Square(row=5, col=4)

        # All Baseclaims that use square_4_0 as the first or third square.
        want_baseclaims = {
            ## Baseclaims where square_4_0 is the first square.
            # Baseclaims where square_5_1 is the second square.
            Baseclaim(first=square_4_0, second=square_5_1, third=square_5_2),  # Useful.
            Baseclaim(first=square_4_0, second=square_5_1, third=square_5_4),  # Useful.
            # Baseclaims where square_5_2 is the second square.
            Baseclaim(first=square_4_0, second=square_5_2, third=square_5_1),  # Useful.
            Baseclaim(first=square_4_0, second=square_5_2, third=square_5_4),  # Useful.
        }
        got_baseclaims = BaseclaimManager._baseclaims_given_first_and_third_square(
            square=square_4_0,
            directly_playable_squares=board.playable_squares(),
        )
        self.assertEqual(want_baseclaims, got_baseclaims)

    def test_baseclaim_given_second_square_directly_playable_odd(self):
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

        # Directly playable squares.
        square_4_0 = Square(row=4, col=0)
        square_5_1 = Square(row=5, col=1)
        square_5_2 = Square(row=5, col=2)
        square_5_4 = Square(row=5, col=4)

        want_baseclaims = {
            Baseclaim(first=square_4_0, second=square_5_1, third=square_5_2),
            Baseclaim(first=square_4_0, second=square_5_1, third=square_5_4),
        }

        got_baseclaims = BaseclaimManager._baseclaims_given_second_square(
            second=square_5_1,
            directly_playable_squares=board.playable_squares(),
        )
        self.assertEqual(want_baseclaims, got_baseclaims)

    def test_baseclaim_given_second_square_directly_playable_even(self):
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

        # Since the second square is even, an empty set should be returned.
        got_baseclaims = BaseclaimManager._baseclaims_given_second_square(
            second=Square(row=4, col=0),
            directly_playable_squares=board.playable_squares(),
        )
        self.assertFalse(got_baseclaims)

    # Tests for when second is not in directly_playable_squares and generates no new Baseclaims.
    def test_baseclaim_given_second_square_even_above_directly_playable(self):
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

        # Since the second square is even, an empty set should be returned.
        got_baseclaims = BaseclaimManager._baseclaims_given_second_square(
            second=Square(row=4, col=1),
            directly_playable_squares=board.playable_squares(),
        )
        self.assertFalse(got_baseclaims)

    def test_find_problems_solved_for_player(self):
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
        pm = ConnectFourGroupManager(env_variables=self.env.env_variables)

        # Baseclaim b1-c1-c2-e1 can be used to refute b1-e4 and c1-f1.
        baseclaim_b1_c1_c2_f1 = Baseclaim(
            first=Square(row=5, col=1),  # b1
            second=Square(row=5, col=2),  # c1
            third=Square(row=5, col=4),  # e1
        )

        want_problems_solved_for_player_0 = {
            Group(player=0, start=Square(row=5, col=1), end=Square(row=2, col=4)),  # b1-e4
            Group(player=0, start=Square(row=5, col=2), end=Square(row=5, col=5)),  # c1-f1
            Group(player=0, start=Square(row=5, col=1), end=Square(row=5, col=4)),  # b1-e1
        }
        got_problems_solved_for_player_0 = baseclaim_b1_c1_c2_f1.find_problems_solved_for_player(
            groups_by_square=pm.groups_by_square_by_player[0],
        )
        self.assertEqual(want_problems_solved_for_player_0, got_problems_solved_for_player_0)

    def test_solves(self):
        # Baseclaim b1-c1-c2-e1 allows the player to guarantee themselves one of the following squares:
        # 1. b1 or c2
        # 2. c1 or e1
        # c2 is the non-playable square.
        baseclaim_b1_c1_c2_f1 = Baseclaim(
            first=Square(row=5, col=1),  # b1
            second=Square(row=5, col=2),  # c1
            third=Square(row=5, col=4),  # e1
        )

        # Group b1-e4 contains b1 and c2, so the Baseclaim can refute it.
        white_group_b1_e4 = Group(player=0, start=Square(row=5, col=1), end=Square(row=2, col=4))  # b1-e4
        self.assertTrue(baseclaim_b1_c1_c2_f1.solves(group=white_group_b1_e4))
        # Group c1-f1 contains c1 and e1, so the Baseclaim can refute it.
        white_group_c1_f1 = Group(player=0, start=Square(row=5, col=2), end=Square(row=5, col=5))  # c1-f1
        self.assertTrue(baseclaim_b1_c1_c2_f1.solves(group=white_group_c1_f1))
        # Group c2-f2 does not contain b1 and c2 and it does not contain c1 and e1, so the Baseclaim cannot refute it.
        white_group_c2_f2 = Group(player=0, start=Square(row=4, col=2), end=Square(row=4, col=5))  # c2-f2
        self.assertFalse(baseclaim_b1_c1_c2_f1.solves(group=white_group_c2_f2))

    def test_is_useful(self):
        baseclaim_b1_c1_c2_f1 = Baseclaim(
            first=Square(row=5, col=1),  # b1
            second=Square(row=5, col=2),  # c1
            third=Square(row=5, col=4),  # e1
        )

        # Group b1-e4 contains b1 and c2, so the Baseclaim can refute it.
        white_group_b1_e4 = Group(player=0, start=Square(row=5, col=1), end=Square(row=2, col=4))  # b1-e4

        # If a Baseclaim solves at least one Group, it is useful.
        self.assertTrue(baseclaim_b1_c1_c2_f1.is_useful(groups={white_group_b1_e4}))
        self.assertFalse(baseclaim_b1_c1_c2_f1.is_useful(groups=set()))


if __name__ == '__main__':
    unittest.main()
