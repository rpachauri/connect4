import gym
import unittest

import numpy as np

from connect_four.game import Square
from connect_four.problem import Group
from connect_four.evaluation.victor.board import Board
from connect_four.envs.connect_four_env import ConnectFourEnv


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 4
        ConnectFourEnv.N = 4
        self.env.reset()

    def test_is_empty(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        self.assertTrue(board.is_empty(Square(0, 0)))
        self.assertFalse(board.is_empty(Square(3, 3)))
        self.assertFalse(board.is_empty(Square(3, 2)))

    def test_playable_square(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        self.assertEqual(Square(3, 0), board.playable_square(0))

    def test_playable_squares(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        want_squares = {
            Square(3, 0),
            Square(3, 1),
            Square(2, 2),
            Square(2, 3),
        }
        self.assertEqual(want_squares, board.playable_squares())

    def test_is_potential_group(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
                [1, 0, 0, 1, ],
                [0, 1, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 1, 0, ],
                [0, 1, 1, 0, ],
                [1, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        self.assertTrue(board.is_valid(Square(row=0, col=3)))
        self.assertTrue(board.is_valid(Square(row=1, col=3)))
        self.assertTrue(board.is_valid(Square(row=2, col=3)))
        self.assertTrue(board.is_valid(Square(row=3, col=3)))
        self.assertTrue(board.is_potential_group(player=0, row=0, col=3, row_diff=1, col_diff=0))

    def test_potential_groups(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
                [1, 0, 0, 1, ],
                [0, 1, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 1, 0, ],
                [0, 1, 1, 0, ],
                [1, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        want_groups_player0 = {
            Group(0, Square(0, 0), Square(0, 3)),
            Group(0, Square(0, 3), Square(3, 3)),
        }
        self.assertEqual(want_groups_player0, board.potential_groups(0))
        want_groups_player1 = {
            Group(1, Square(0, 0), Square(0, 3)),
            Group(1, Square(0, 3), Square(3, 0)),
            Group(1, Square(0, 2), Square(3, 2)),
        }
        self.assertEqual(want_groups_player1, board.potential_groups(1))

    def test_potential_groups_by_square(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
                [1, 0, 0, 1, ],
                [0, 1, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 1, 0, ],
                [0, 1, 1, 0, ],
                [1, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        group_0_0_to_0_3 = Group(0, Square(0, 0), Square(0, 3))
        group_0_3_to_3_3 = Group(0, Square(0, 3), Square(3, 3))

        want_groups_by_square = {
            # Column 0.
            Square(row=0, col=0): {group_0_0_to_0_3},
            Square(row=1, col=0): set(),
            Square(row=2, col=0): set(),
            Square(row=3, col=0): set(),
            # Column 1.
            Square(row=0, col=1): {group_0_0_to_0_3},
            Square(row=1, col=1): set(),
            Square(row=2, col=1): set(),
            Square(row=3, col=1): set(),
            # Column 2.
            Square(row=0, col=2): {group_0_0_to_0_3},
            Square(row=1, col=2): set(),
            Square(row=2, col=2): set(),
            Square(row=3, col=2): set(),
            # Column 3.
            Square(row=0, col=3): {group_0_0_to_0_3, group_0_3_to_3_3},
            Square(row=1, col=3): {group_0_3_to_3_3},
            Square(row=2, col=3): {group_0_3_to_3_3},
            Square(row=3, col=3): {group_0_3_to_3_3},
        }
        got_groups_by_square = board.potential_groups_by_square()
        self.assertEqual(want_groups_by_square, got_groups_by_square)

    def test_empty_squares(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 1, ],
                [1, 0, 0, 1, ],
                [1, 0, 1, 0, ],
                [0, 1, 0, 1, ],
            ],
            [
                [0, 0, 1, 0, ],
                [0, 1, 1, 0, ],
                [0, 1, 0, 1, ],
                [1, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        want_empty_squares = {
            Square(row=0, col=0),  # a4
            Square(row=0, col=1),  # b4
        }
        got_empty_squares = board.empty_squares()
        self.assertEqual(want_empty_squares, got_empty_squares)


if __name__ == '__main__':
    unittest.main()