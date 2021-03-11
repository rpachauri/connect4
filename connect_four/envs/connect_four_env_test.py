import unittest

import gym
import numpy as np

from connect_four.envs import TwoPlayerGameEnv
from connect_four.envs import ConnectFourEnv

np.set_printoptions(threshold=np.inf)


class TestConnectFourEnv(unittest.TestCase):

    def setUp(self):
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_reset(self):
        obs = self.env.reset()
        # upon initialization, it should be Player 1's turn.
        self.assertEqual(self.env.player_turn, 0)
        # upon initialization, board should be full of 0s.
        self.assertIsNone(np.testing.assert_array_equal(
            obs,
            np.zeros(shape=(2, ConnectFourEnv.M, ConnectFourEnv.N)),
        ))

    def test_find_highest_token(self):
        # place a token for Player 1 in the first column.
        self.env.state[0, -1, 0] = 1
        # fill the entire 2nd column with tokens belonging to Player 2.
        self.env.state[1, :, 1] = 1

        # when there is only 1 token in the column,
        # the highest token should be at the lowest row.
        self.assertEqual(self.env._find_highest_token(0), ConnectFourEnv.M - 1)
        # when the column is full,
        # the highest token should be at the highest row.
        self.assertEqual(self.env._find_highest_token(1), 0)
        # when the column is empty,
        # the highest token should be ConnectFourEnv.M.
        self.assertEqual(self.env._find_highest_token(2), ConnectFourEnv.M)

    def test_place_token_in_full_column(self):
        # fill the entire 2nd column with tokens belonging to Player 2.
        self.env.state[1, :, 1] = 1
        state_copy = self.env.state.copy()

        obs, reward, done, _ = self.env.step(1)
        # verify that the state has not changed.
        self.assertIsNone(np.testing.assert_array_equal(
            obs,
            state_copy,
        ))
        # verify the expected reward.
        self.assertEqual(reward, ConnectFourEnv.INVALID_MOVE)
        # verify the environment is done.
        self.assertTrue(done)

    def test_place_token_and_connected_four(self):
        self.env.state[0, -3:, 0] = 1
        expected_state = self.env.state.copy()
        expected_state[0, -4, 0] = 1

        obs, reward, done, _ = self.env.step(0)
        # verify that the state has not changed.
        self.assertIsNone(np.testing.assert_array_equal(
            obs,
            expected_state,
        ))
        # verify the expected reward.
        self.assertEqual(reward, ConnectFourEnv.CONNECTED_FOUR)
        # verify the environment is done.
        self.assertTrue(done)

    def test_is_full(self):
        # Place a token for Player 1 in the first column.
        self.env.state[0, -1, 0] = 1
        self.assertFalse(self.env._is_full())

        # Cover the entire state with tokens from Player 1.
        self.env.state[0, :, :] = 1
        self.assertTrue(self.env._is_full())

    def test_draw(self):
        # **Note**. This test makes an assumption that env.step(action) only checks
        # if the location of the **new token** results in a win.
        # It assumes the environment does not check any other locations.

        # Make all locations expect the top-left belong to Player 2.
        self.env.state[1, :, :] = 1
        self.env.state[1, 0, 0] = 0

        # We expect there to be a token for Player 1 in the top-left.
        expected_state = self.env.state.copy()
        expected_state[0, 0, 0] = 1

        obs, reward, done, _ = self.env.step(0)
        # verify that the state has not changed.
        self.assertIsNone(np.testing.assert_array_equal(
            obs,
            expected_state,
        ))
        # verify the expected reward.
        self.assertEqual(reward, ConnectFourEnv.DRAW)
        # verify the environment is done.
        self.assertTrue(done)

    def test_continue_playing_after_step(self):
        # We expect there to be a token for Player 1 in the bottom-left.
        expected_state = self.env.state.copy()
        expected_state[0, -1, 0] = 1

        obs, reward, done, _ = self.env.step(0)
        # verify that the state has not changed.
        self.assertIsNone(np.testing.assert_array_equal(
            obs,
            expected_state,
        ))
        # verify the expected reward.
        self.assertEqual(reward, TwoPlayerGameEnv.DEFAULT_REWARD)
        # verify the environment is done.
        self.assertFalse(done)
        # verify it is Player 2's turn.
        self.assertEqual(self.env.player_turn, 1)

        # We expect there to be a token for Player 2 above Player 1's token.
        expected_state[1, -2, 0] = 1
        obs, reward, done, _ = self.env.step(0)
        # verify that the state has not changed.
        self.assertIsNone(np.testing.assert_array_equal(
            obs,
            expected_state,
        ))
        # verify the expected reward.
        self.assertEqual(reward, TwoPlayerGameEnv.DEFAULT_REWARD)
        # verify the environment is done.
        self.assertFalse(done)
        # verify it is Player 2's turn.
        self.assertEqual(self.env.player_turn, 0)

    def test_get_env_variables(self):
        # Seed the environment so we can verify we can reset to an arbitrary state.
        self.env.step(0)

        # Retrieve the env variables.
        env_variables = self.env.env_variables

        # Modify the environment.
        obs, _, _, _ = self.env.step(0)

        # Verify that the state has changed.
        np.testing.assert_raises(
            AssertionError, np.testing.assert_array_equal, obs, env_variables[0])

        # reset the state to previously saved env_variables.
        obs = self.env.reset(env_variables=env_variables)
        # verify that the state is back to what it was after Player 2 moved.
        self.assertIsNone(np.testing.assert_array_equal(
            obs,
            env_variables[0],
        ))
        # verify it is currently Player 1's turn.
        self.assertEqual(self.env.player_turn, env_variables[1])

    def test_undo_last_action_initial_state(self):
        # This test validates that undo_last_action does not work on the initial state.
        raises = False
        try:
            self.env.undo_last_action(0)
        except ValueError:
            raises = True
        self.assertTrue(raises)

    def test_undo_last_action_empty_column(self):
        # This test validates that undo_last_action does not work on an empty column.
        # Seed the environment so it doesn't fail undoing the initial state.
        self.env.step(0)

        raises = False
        try:
            # Undo an action on an empty column.
            self.env.undo_last_action(1)
        except ValueError:
            raises = True
        self.assertTrue(raises)

    def test_undo_last_action_same_player(self):
        # This test validates that undo_last_action does not work on a column where the top
        # token belongs to the current player.
        # Seed the environment.
        self.env.step(0)
        self.env.step(1)
        # It is currently White's turn.

        raises = False
        try:
            # Undo an action on a column in which White has the top token.
            self.env.undo_last_action(0)
        except ValueError:
            raises = True
        self.assertTrue(raises)

    def test_undo_last_action_after_single_move(self):
        # This test validates that undo_last_action works after a single move.

        # Retrieve the desired env variables.
        want_env_variables = self.env.env_variables

        # Make a move.
        self.env.step(0)
        # Undo the move.
        self.env.undo_last_action(action=0)

        # Retrieve the env variables after undoing the move.
        got_env_variables = self.env.env_variables

        # verify that the state is back to what it was after Player 2 moved.
        self.assertIsNone(np.testing.assert_array_equal(
            want_env_variables[0],
            got_env_variables[0],
        ))
        # verify it is currently Player 1's turn.
        self.assertEqual(want_env_variables[1], got_env_variables[1])


if __name__ == '__main__':
    unittest.main()
