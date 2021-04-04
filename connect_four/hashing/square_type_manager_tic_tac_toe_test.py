import gym
import unittest

import numpy as np

from connect_four.hashing.data_structures import Group, Square
from connect_four.hashing.square_type_manager import SquareTypeManager


class TestSquareTypeManagerTicTacToe(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('tic_tac_toe-v0')

    def test_remove_groups(self):
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)
        # It should be Player 1's turn.
        self.assertEqual(0, stm.player)

        # In this test case, we're going to remove groups that contain 00 for Player 2.
        group_00_to_02 = Group(squares=frozenset([Square(row=0, col=0), Square(row=0, col=1), Square(row=0, col=2)]))
        group_00_to_22 = Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=1), Square(row=2, col=2)]))
        group_00_to_20 = Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=0), Square(row=2, col=0)]))
        want_groups_removed_by_square = {
            Square(row=0, col=0): {group_00_to_02, group_00_to_22, group_00_to_20},
            Square(row=0, col=1): {group_00_to_02},
            Square(row=0, col=2): {group_00_to_02},
            Square(row=1, col=1): {group_00_to_22},
            Square(row=2, col=2): {group_00_to_22},
            Square(row=1, col=0): {group_00_to_20},
            Square(row=2, col=0): {group_00_to_20},
        }

        # Remove groups that contain 00 for Player 2.
        got_groups_removed_by_square = stm._remove_groups(opponent=1, row=0, col=0)
        self.assertEqual(want_groups_removed_by_square, got_groups_removed_by_square)

    def test_find_indifferent_squares(self):
        self.env.state = np.array([
            [
                [1, 0, 1, ],
                [1, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 1, 0, ],
                [0, 1, 0, ],
                [1, 0, 0, ],
            ],
        ])
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)

        # Player 1 plays in the bottom-middle square.
        # Remove groups that contain 21 for Player 2.
        groups_removed_by_square = stm._remove_groups(opponent=1, row=2, col=1)

        want_indifferent_squares = {
            Square(row=0, col=1),  # top-middle
            Square(row=1, col=1),  # center
            Square(row=2, col=0),  # bottom-left
            Square(row=2, col=1),  # bottom-middle
        }
        got_indifferent_squares = stm._find_indifferent_squares(
            row=2,
            col=1,
            groups_removed_by_square=groups_removed_by_square,
        )
        self.assertEqual(want_indifferent_squares, got_indifferent_squares)


if __name__ == '__main__':
    unittest.main()
