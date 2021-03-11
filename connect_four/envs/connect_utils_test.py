import unittest

import numpy as np

from connect_four.envs import connect_utils


class TestConnectUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.M = 4
        self.N = 4
        self.state = np.zeros(shape=(2, self.M, self.N))

    def test_num_tokens_in_direction(self):
        # fill the entire 1st column with tokens belonging to Player 1.
        self.state[0, :, 0] = 1

        num_tokens = connect_utils._num_tokens_in_direction(
            state=self.state,
            player=0,
            row=0,
            col=0,
            row_add=1,
            col_add=0,
        )
        # since the entire column has been filled, there should be self.M - 1 tokens.
        # We exclude the passe in square.
        self.assertEqual(num_tokens, self.M - 1)

    def test_connected_vertically(self):
        # fill the entire 1st column with tokens belonging to Player 1.
        # Player 1 should have connected M starting with (0, 0).
        self.state[0, :, 0] = 1
        self.assertTrue(connect_utils.connected(
            state=self.state,
            num_to_connect=self.M,
            player=0,
            row=0,
            col=0,
        ))

    def test_connected_left_diagonally(self):
        # Place a token for Player 1 left-diagonally starting from (0, 0).
        # Player 1 should have connected M starting with (0, 0).
        for i in range(min(self.M, self.N)):
            self.state[0, i, i] = 1
        self.assertTrue(connect_utils.connected(
            state=self.state,
            num_to_connect=self.M,
            player=0,
            row=0,
            col=0,
        ))

    def test_connected_four_horizontally(self):
        # fill the entire bottom row with tokens belonging to Player 1.
        self.state[0, self.M - 1, :] = 1
        # If starting from the bottom-right token,
        # verify that Player 1 has connected N.
        self.assertTrue(connect_utils.connected(
            state=self.state,
            num_to_connect=self.N,
            player=0,
            row=self.M - 1,
            col=self.N - 1,
        ))

    def test_has_not_connected_four(self):
        self.state[0, 0, 0] = 1
        self.assertFalse(connect_utils.connected(
            state=self.state,
            num_to_connect=self.M,
            player=0,
            row=0,
            col=0,
        ))


if __name__ == '__main__':
    unittest.main()
