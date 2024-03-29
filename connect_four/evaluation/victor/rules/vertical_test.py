import gym
import unittest

import numpy as np

from connect_four.evaluation.victor.rules.vertical import VerticalManager
from connect_four.game import Square
from connect_four.evaluation.board import Board
from connect_four.evaluation.victor.rules import Vertical
from connect_four.evaluation.victor.rules import find_all_verticals
from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.problem import Group
from connect_four.problem import ConnectFourGroupManager


class TestVertical(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_vertical(self):
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
        got_verticals = find_all_verticals(board)

        want_verticals = {
            # First column.
            Vertical(Square(1, 0), Square(2, 0)),
            Vertical(Square(3, 0), Square(4, 0)),
            # Second column.
            Vertical(Square(1, 1), Square(2, 1)),
            Vertical(Square(3, 1), Square(4, 1)),
            # Fourth column.
            Vertical(Square(1, 3), Square(2, 3)),
            # Fifth column.
            Vertical(Square(1, 4), Square(2, 4)),
            # Sixth column.
            Vertical(Square(1, 5), Square(2, 5)),
            Vertical(Square(3, 5), Square(4, 5)),
            # Seventh column.
            Vertical(Square(1, 6), Square(2, 6)),
            Vertical(Square(3, 6), Square(4, 6)),
        }
        self.assertEqual(want_verticals, got_verticals)

    def test_vertical_manager_initialization(self):
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
        vm = VerticalManager(board=board)
        got_verticals = vm.verticals

        want_verticals = {
            # First column.
            Vertical(Square(1, 0), Square(2, 0)),
            Vertical(Square(3, 0), Square(4, 0)),
            # Second column.
            Vertical(Square(1, 1), Square(2, 1)),
            Vertical(Square(3, 1), Square(4, 1)),
            # Fourth column.
            Vertical(Square(1, 3), Square(2, 3)),
            # Fifth column.
            Vertical(Square(1, 4), Square(2, 4)),
            # Sixth column.
            Vertical(Square(1, 5), Square(2, 5)),
            Vertical(Square(3, 5), Square(4, 5)),
            # Seventh column.
            Vertical(Square(1, 6), Square(2, 6)),
            Vertical(Square(3, 6), Square(4, 6)),
        }
        self.assertEqual(want_verticals, got_verticals)

    def test_move_undo_move(self):
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
        vm = VerticalManager(board=board)

        # White will play at e4, removing Vertical e4-e5.
        vertical = Vertical(
            lower=Square(row=2, col=4),  # e4
            upper=Square(row=1, col=4),  # e5
        )
        got_removed_vertical = vm.move(square=Square(row=2, col=4))  # e4
        self.assertEqual(vertical, got_removed_vertical)

        # Undo White's move at e4, adding Vertical e4-e5.
        got_added_vertical = vm.undo_move(square=Square(row=2, col=4))  # e4
        self.assertEqual(vertical, got_added_vertical)

    def test_move_undo_move_odd_square(self):
        board = Board(self.env.env_variables)
        vm = VerticalManager(board=board)

        # White plays at a1. No verticals should be removed.
        got_removed_vertical = vm.move(square=Square(row=5, col=0))  # a1
        self.assertIsNone(got_removed_vertical)

        # Undo White's move at a2. No verticals should be added.
        got_added_vertical = vm.undo_move(square=Square(row=5, col=0))  # a1
        self.assertIsNone(got_added_vertical)

    def test_move_undo_move_top_row(self):
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
        vm = VerticalManager(board=board)

        # White plays at c6. No verticals should be removed.
        got_removed_vertical = vm.move(square=Square(row=0, col=2))  # c6
        self.assertIsNone(got_removed_vertical)

        # Undo White's move at c6. No verticals should be added.
        got_added_vertical = vm.undo_move(square=Square(row=0, col=2))  # c6
        self.assertIsNone(got_added_vertical)

    def test_find_problems_solved(self):
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
        pm = ConnectFourGroupManager(env_variables=self.env.env_variables)

        # The Vertical e4-e5 solves e2-e5 and e3-e6.
        vertical_e4_e5 = Vertical(upper=Square(row=2, col=4), lower=Square(row=1, col=4))

        want_problems_solved = {
            # Groups that belong to White. These were included in the original paper.
            Group(player=0, start=Square(row=4, col=4), end=Square(row=1, col=4)),  # e2-e5
            Group(player=0, start=Square(row=3, col=4), end=Square(row=0, col=4)),  # e3-e6
            # There are no Groups that belong to Black this vertical solves.
        }
        got_problems_solved = vertical_e4_e5.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_problems_solved, got_problems_solved)

    def test_solves(self):
        # The Vertical e4-e5 solves e2-e5 but not e1-e4.
        vertical_e4_e5 = Vertical(upper=Square(row=2, col=4), lower=Square(row=1, col=4))

        white_group_e2_e5 = Group(player=0, start=Square(row=4, col=4), end=Square(row=1, col=4))  # e2-e5
        white_group_e1_e4 = Group(player=0, start=Square(row=5, col=4), end=Square(row=2, col=4))  # e1-e4

        self.assertTrue(vertical_e4_e5.solves(group=white_group_e2_e5))
        self.assertFalse(vertical_e4_e5.solves(group=white_group_e1_e4))

    def test_is_useful(self):
        vertical_e4_e5 = Vertical(upper=Square(row=2, col=4), lower=Square(row=1, col=4))

        white_group_e2_e5 = Group(player=0, start=Square(row=4, col=4), end=Square(row=1, col=4))  # e2-e5

        # If a Vertical solves at least one Group, it is useful.
        self.assertTrue(vertical_e4_e5.is_useful(groups={white_group_e2_e5}))
        self.assertFalse(vertical_e4_e5.is_useful(groups=set()))


if __name__ == '__main__':
    unittest.main()
