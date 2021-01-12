import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Threat
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

    def test_is_potential_threat(self):
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
        self.assertTrue(board.is_potential_threat(player=0, row=0, col=3, row_diff=1, col_diff=0))

    def test_potential_threats(self):
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
        want_threats_player0 = {
            Threat(0, Square(0, 0), Square(0, 3)),
            Threat(0, Square(0, 3), Square(3, 3)),
        }
        self.assertEqual(want_threats_player0, board.potential_threats(0))
        want_threats_player1 = {
            Threat(1, Square(0, 0), Square(0, 3)),
            Threat(1, Square(0, 3), Square(3, 0)),
            Threat(1, Square(0, 2), Square(3, 2)),
        }
        self.assertEqual(want_threats_player1, board.potential_threats(1))

    def test_potential_threats_by_square(self):
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
        threat_0_0_to_0_3 = Threat(0, Square(0, 0), Square(0, 3))
        threat_0_3_to_3_3 = Threat(0, Square(0, 3), Square(3, 3))

        want_threats_by_square = {
            # Column 0.
            Square(row=0, col=0): {threat_0_0_to_0_3},
            Square(row=1, col=0): set(),
            Square(row=2, col=0): set(),
            Square(row=3, col=0): set(),
            # Column 1.
            Square(row=0, col=1): {threat_0_0_to_0_3},
            Square(row=1, col=1): set(),
            Square(row=2, col=1): set(),
            Square(row=3, col=1): set(),
            # Column 2.
            Square(row=0, col=2): {threat_0_0_to_0_3},
            Square(row=1, col=2): set(),
            Square(row=2, col=2): set(),
            Square(row=3, col=2): set(),
            # Column 3.
            Square(row=0, col=3): {threat_0_0_to_0_3, threat_0_3_to_3_3},
            Square(row=1, col=3): {threat_0_3_to_3_3},
            Square(row=2, col=3): {threat_0_3_to_3_3},
            Square(row=3, col=3): {threat_0_3_to_3_3},
        }
        got_threats_by_square = board.potential_threats_by_square()
        self.assertEqual(want_threats_by_square, got_threats_by_square)


if __name__ == '__main__':
    unittest.main()