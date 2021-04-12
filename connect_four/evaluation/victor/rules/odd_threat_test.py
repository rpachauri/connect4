import unittest

import gym
import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.rules import OddThreat
from connect_four.evaluation.victor.rules import find_all_odd_threats
from connect_four.game import Square
from connect_four.problem import Group
from connect_four.problem import ConnectFourProblemManager


class TestOddThreat(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_no_odd_threat_exists(self):
        # There is no odd Threat for an empty Board.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_odd_threats = find_all_odd_threats(board=board)
        self.assertFalse(got_odd_threats)

    def test_find_odd_threat(self):
        # This test is based on Diagram 8.1 from the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [1, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        want_odd_threats = {
            OddThreat(
                group=Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
                empty_square=Square(row=3, col=0),  # a3
                directly_playable_square=Square(row=4, col=0),  # a2
            ),
        }
        got_odd_threats = find_all_odd_threats(board=board)
        self.assertEqual(want_odd_threats, got_odd_threats)

    def test_find_odd_threat_when_multiple_exist(self):
        # There are two odd Threats in the 3rd row from the bottom.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        want_odd_threats = {
            OddThreat(
                group=Group(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
                empty_square=Square(row=3, col=1),  # b3
                directly_playable_square=Square(row=5, col=1),  # b1
            ),
            OddThreat(
                group=Group(player=0, start=Square(row=3, col=2), end=Square(row=3, col=5)),  # c3-f3
                empty_square=Square(row=3, col=5),  # f3
                directly_playable_square=Square(row=5, col=5),  # f1
            ),
        }
        got_odd_threats = find_all_odd_threats(board=board)
        self.assertEqual(want_odd_threats, got_odd_threats)

    def test_find_problems_solved(self):
        # This test case is based on Diagram 8.2.
        # Black is to move and White has an odd threat at a3.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1  # Black to move.
        pm = ConnectFourProblemManager(env_variables=self.env.env_variables)

        odd_threat_a3_d3 = OddThreat(
            group=Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
            empty_square=Square(row=3, col=0),  # a3
            directly_playable_square=Square(row=5, col=0),  # a1
        )

        want_problems_solved = {
            # a1 is a directly playable odd square, so we include all Groups that contain a1.
            Group(player=1, start=Square(row=5, col=0), end=Square(row=2, col=0)),  # a1-a4
            # Starting from a3 and up, any Group that contains a square in the a-column is included.
            # Groups that contain a3.
            Group(player=1, start=Square(row=4, col=0), end=Square(row=1, col=0)),  # a2-a5
            Group(player=1, start=Square(row=3, col=0), end=Square(row=0, col=0)),  # a3-a6
            Group(player=1, start=Square(row=3, col=0), end=Square(row=0, col=3)),  # a3-d6
            # Groups that contain a4.
            Group(player=1, start=Square(row=2, col=0), end=Square(row=2, col=3)),  # a4-d4
            # Groups that contain a5.
            Group(player=1, start=Square(row=1, col=0), end=Square(row=1, col=3)),  # a5-d5
            # Groups that contain a6.
            Group(player=1, start=Square(row=0, col=0), end=Square(row=0, col=3)),  # a6-d6
        }
        got_problems_solved = odd_threat_a3_d3.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_problems_solved, got_problems_solved)

    def test_diagram_7_2(self):
        # This test case is based on Diagram 5.4 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 1, 1, ],
                [0, 0, 1, 1, 0, 1, 0, ],
                [0, 0, 0, 0, 1, 1, 1, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 1, 0, ],
            ],
            [
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 1, 1, ],
                [0, 0, 0, 0, 1, 1, 0, ],
                [0, 1, 1, 0, 0, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)

        got_odd_threats = find_all_odd_threats(board=board)
        self.assertFalse(got_odd_threats)


if __name__ == '__main__':
    unittest.main()
