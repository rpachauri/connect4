import gym
import unittest

import numpy as np

from connect_four.evaluation.victor.rules.baseinverse import BaseinverseManager
from connect_four.game import Square
from connect_four.evaluation.board import Board

from connect_four.evaluation.victor.rules import Baseinverse
from connect_four.evaluation.victor.rules import find_all_baseinverses

from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.problem import Group
from connect_four.problem import ConnectFourGroupManager


class TestBaseinverse(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_baseinverse(self):
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
        got_baseinverses = find_all_baseinverses(board)

        want_baseinverses = {
            # All matches with Square(5, 0).
            Baseinverse(Square(5, 0), Square(5, 1)),  # a1-b1
            # Baseinverse(Square(5, 0), Square(2, 2)),  # a1-c4
            # Baseinverse(Square(5, 0), Square(3, 3)),  # a1-d3
            # Baseinverse(Square(5, 0), Square(4, 4)),  # a1-e2
            # Baseinverse(Square(5, 0), Square(5, 5)),  # a1-f1
            # Baseinverse(Square(5, 0), Square(5, 6)),  # a1-g1
            # All matches with Square(5, 1).
            # Baseinverse(Square(5, 1), Square(2, 2)),  # b1-c4
            Baseinverse(Square(5, 1), Square(3, 3)),  # b1-d3
            # Baseinverse(Square(5, 1), Square(4, 4)),  # b1-e2
            # Baseinverse(Square(5, 1), Square(5, 5)),  # b1-f1
            # Baseinverse(Square(5, 1), Square(5, 6)),  # b1-g1
            # All matches with Square(2, 2).
            Baseinverse(Square(2, 2), Square(3, 3)),  # c4-d3
            Baseinverse(Square(2, 2), Square(4, 4)),  # c4-e2
            Baseinverse(Square(2, 2), Square(5, 5)),  # c4-f1
            # Baseinverse(Square(2, 2), Square(5, 6)),  # c4-g1
            # All matches with Square(3, 3).
            Baseinverse(Square(3, 3), Square(4, 4)),  # d3-e2
            Baseinverse(Square(3, 3), Square(5, 5)),  # d3-f1
            # Baseinverse(Square(3, 3), Square(5, 6)),  # d3-g1
            # All matches with Square(4, 4).
            Baseinverse(Square(4, 4), Square(5, 5)),  # e2-f1
            # Baseinverse(Square(4, 4), Square(5, 6)),  # e2-g1
            # All matches with Square(5, 5).
            Baseinverse(Square(5, 5), Square(5, 6)),  # f1-g1
        }
        self.assertEqual(want_baseinverses, got_baseinverses)

    def test_baseinverse_manager_initialization(self):
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
        bm = BaseinverseManager(board=board)
        got_baseinverses = bm.baseinverses

        want_baseinverses = {
            # All matches with Square(5, 0).
            Baseinverse(Square(5, 0), Square(5, 1)),  # a1-b1
            # Baseinverse(Square(5, 0), Square(2, 2)),  # a1-c4
            # Baseinverse(Square(5, 0), Square(3, 3)),  # a1-d3
            # Baseinverse(Square(5, 0), Square(4, 4)),  # a1-e2
            # Baseinverse(Square(5, 0), Square(5, 5)),  # a1-f1
            # Baseinverse(Square(5, 0), Square(5, 6)),  # a1-g1
            # All matches with Square(5, 1).
            # Baseinverse(Square(5, 1), Square(2, 2)),  # b1-c4
            Baseinverse(Square(5, 1), Square(3, 3)),  # b1-d3
            # Baseinverse(Square(5, 1), Square(4, 4)),  # b1-e2
            # Baseinverse(Square(5, 1), Square(5, 5)),  # b1-f1
            # Baseinverse(Square(5, 1), Square(5, 6)),  # b1-g1
            # All matches with Square(2, 2).
            Baseinverse(Square(2, 2), Square(3, 3)),  # c4-d3
            Baseinverse(Square(2, 2), Square(4, 4)),  # c4-e2
            Baseinverse(Square(2, 2), Square(5, 5)),  # c4-f1
            # Baseinverse(Square(2, 2), Square(5, 6)),  # c4-g1
            # All matches with Square(3, 3).
            Baseinverse(Square(3, 3), Square(4, 4)),  # d3-e2
            Baseinverse(Square(3, 3), Square(5, 5)),  # d3-f1
            # Baseinverse(Square(3, 3), Square(5, 6)),  # d3-g1
            # All matches with Square(4, 4).
            Baseinverse(Square(4, 4), Square(5, 5)),  # e2-f1
            # Baseinverse(Square(4, 4), Square(5, 6)),  # e2-g1
            # All matches with Square(5, 5).
            Baseinverse(Square(5, 5), Square(5, 6)),  # f1-g1
        }
        self.assertEqual(want_baseinverses, got_baseinverses)

    def test_move(self):
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
        bm = BaseinverseManager(board=board)

        # White will play at a1, removing any Baseinverses that include a1 and adding any Baseinverses that include a2.

        want_removed_baseinverses = {
            Baseinverse(Square(5, 0), Square(5, 1)),  # a1-b1
            # Baseinverse(Square(5, 0), Square(2, 2)),  # a1-c4
            # Baseinverse(Square(5, 0), Square(3, 3)),  # a1-d3
            # Baseinverse(Square(5, 0), Square(4, 4)),  # a1-e2
            # Baseinverse(Square(5, 0), Square(5, 5)),  # a1-f1
            # Baseinverse(Square(5, 0), Square(5, 6)),  # a1-g1
        }
        want_added_baseinverses = {
            # Baseinverse(Square(4, 0), Square(5, 1)),  # a2-b1
            Baseinverse(Square(4, 0), Square(2, 2)),  # a2-c4
            # Baseinverse(Square(4, 0), Square(3, 3)),  # a2-d3
            # Baseinverse(Square(4, 0), Square(4, 4)),  # a2-e2
            # Baseinverse(Square(4, 0), Square(5, 5)),  # a2-f1
            # Baseinverse(Square(4, 0), Square(5, 6)),  # a2-g1
        }

        got_removed_baseinverses, got_added_baseinverses = bm.move(
            square=Square(5, 0),
            playable_squares=board.playable_squares(),
        )
        self.assertEqual(want_removed_baseinverses, got_removed_baseinverses)
        self.assertEqual(want_added_baseinverses, got_added_baseinverses)

    def test_move_top_row(self):
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
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        bm = BaseinverseManager(board=board)

        # White will play at d6.
        # This does not remove or add any Baseinverses.
        got_removed_baseinverses, got_added_baseinverses = bm.move(
            square=Square(0, 3),
            playable_squares=board.playable_squares(),
        )
        self.assertFalse(got_removed_baseinverses)
        self.assertFalse(got_added_baseinverses)

    def test_undo_move(self):
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
        bm = BaseinverseManager(board=board)

        bm.move(
            square=Square(5, 0),
            playable_squares=board.playable_squares(),
        )

        want_added_baseinverses = {
            Baseinverse(Square(5, 0), Square(5, 1)),  # a1-b1
            # Baseinverse(Square(5, 0), Square(2, 2)),  # a1-c4
            # Baseinverse(Square(5, 0), Square(3, 3)),  # a1-d3
            # Baseinverse(Square(5, 0), Square(4, 4)),  # a1-e2
            # Baseinverse(Square(5, 0), Square(5, 5)),  # a1-f1
            # Baseinverse(Square(5, 0), Square(5, 6)),  # a1-g1
        }
        want_removed_baseinverses = {
            # Baseinverse(Square(4, 0), Square(5, 1)),  # a2-b1
            Baseinverse(Square(4, 0), Square(2, 2)),  # a2-c4
            # Baseinverse(Square(4, 0), Square(3, 3)),  # a2-d3
            # Baseinverse(Square(4, 0), Square(4, 4)),  # a2-e2
            # Baseinverse(Square(4, 0), Square(5, 5)),  # a2-f1
            # Baseinverse(Square(4, 0), Square(5, 6)),  # a2-g1
        }

        got_added_baseinverses, got_removed_baseinverses = bm.undo_move(
            square=Square(5, 0),
            playable_squares=board.playable_squares(),
        )
        self.assertEqual(want_added_baseinverses, got_added_baseinverses)
        self.assertEqual(want_removed_baseinverses, got_removed_baseinverses)

    def test_undo_move_top_row(self):
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
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        bm = BaseinverseManager(board=board)

        # White will play at d6, removing any Baseinverses that include d6 and not adding any Baseinverses.

        bm.undo_move(
            square=Square(0, 3),
            playable_squares=board.playable_squares(),
        )

        # We now undo White's move at d6.
        got_added_baseinverses, got_removed_baseinverses = bm.undo_move(
            square=Square(0, 3),
            playable_squares=board.playable_squares(),
        )
        self.assertFalse(got_added_baseinverses)
        self.assertFalse(got_removed_baseinverses)

    def test_find_problems_solved(self):
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
        pm = ConnectFourGroupManager(env_variables=self.env.env_variables)

        # The Baseinverse a1-b1 solves a1-d1.
        baseinverse_a1_b1 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=5, col=1))

        want_problems_solved = {
            # Groups that belong to White. These were included in the original paper.
            Group(player=0, start=Square(row=5, col=0), end=Square(row=5, col=3)),  # a1-d1
            # There are no Groups that belong to Black the baseinverse solves.
        }
        got_problems_solved = baseinverse_a1_b1.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_problems_solved, got_problems_solved)

        # As stated in the original paper, the Baseinverse a1-c4 is possible but useless.
        # Thus, it should solve no problems.
        baseinverse_a1_c4 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=2, col=2))
        self.assertFalse(baseinverse_a1_c4.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        ))

    def test_solves(self):
        baseinverse_a1_b1 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=5, col=1))

        # The Baseinverse a1-b1 solves a1-d1.
        white_group_a1_d1 = Group(player=0, start=Square(row=5, col=0), end=Square(row=5, col=3))  # a1-d1

        self.assertTrue(baseinverse_a1_b1.solves(group=white_group_a1_d1))

        # The Baseinverse a1-b1 does not solve b1-e1.
        white_group_b1_e1 = Group(player=0, start=Square(row=5, col=1), end=Square(row=5, col=4))  # b1-e1
        self.assertFalse(baseinverse_a1_b1.solves(group=white_group_b1_e1))

    def test_is_useful(self):
        baseinverse_a1_b1 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=5, col=1))

        white_group_a1_d1 = Group(player=0, start=Square(row=5, col=0), end=Square(row=5, col=3))  # a1-d1

        # If a Baseinverse solves at least one Group, it is useful.
        self.assertTrue(baseinverse_a1_b1.is_useful(groups={white_group_a1_d1}))
        self.assertFalse(baseinverse_a1_b1.is_useful(groups=set()))


if __name__ == '__main__':
    unittest.main()
