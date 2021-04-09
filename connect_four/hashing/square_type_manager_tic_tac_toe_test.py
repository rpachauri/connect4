import gym
import unittest

import numpy as np

from connect_four.game import Square
from connect_four.hashing.square_type_manager import SquareTypeManager, SquareType


class TestSquareTypeManagerTicTacToe(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('tic_tac_toe-v0')

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
        affected_squares = stm.problem_manager._remove_groups(opponent=1, row=2, col=1)

        want_indifferent_squares = {
            Square(row=0, col=1),  # top-middle
            Square(row=1, col=1),  # center
            Square(row=2, col=0),  # bottom-left
            Square(row=2, col=1),  # bottom-middle
        }
        got_indifferent_squares = stm._find_indifferent_squares(
            player=0,
            row=2,
            col=1,
            affected_squares=affected_squares,
        )
        self.assertEqual(want_indifferent_squares, got_indifferent_squares)

    def test_move_previous_square_types_indifferent_squares(self):
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
        stm.move(
            row=2,
            col=1,
        )
        want_previous_square_types = {
            Square(row=0, col=1): SquareType.Player2,  # top-middle
            Square(row=1, col=1): SquareType.Player2,  # center
            Square(row=2, col=0): SquareType.Player2,  # bottom-left
            Square(row=2, col=1): SquareType.Empty,
        }
        self.assertEqual(want_previous_square_types, stm.previous_square_types_by_move[-1])

    def test_move(self):
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)
        stm.move(row=0, col=0)
        # Validate that play has switched to the opponent.
        self.assertEqual(1, stm.player)
        self.assertEqual(1, len(stm.previous_square_types_by_move))

    def test_undo_move_raises_assertion_error(self):
        # undo_move() should raise an assertion error if the STM is at the given state.
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)
        with self.assertRaises(AssertionError):
            stm.undo_move()

    def test_play_move_undo_move_initial_state(self):
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)

        stm.move(row=0, col=0)
        self.assertEqual(1, stm.player)
        self.assertTrue(stm.previous_square_types_by_move)

        stm.undo_move()
        self.assertEqual(0, stm.player)
        self.assertFalse(stm.previous_square_types_by_move)


if __name__ == '__main__':
    unittest.main()
