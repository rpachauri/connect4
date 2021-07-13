import unittest

import gym
import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.evaluation.board import Board
from connect_four.evaluation.victor.rules import ThreatCombination
from connect_four.evaluation.victor.rules.threat_combination import ThreatCombinationType, find_all_threat_combinations
from connect_four.game import Square
from connect_four.problem import Group
from connect_four.problem import ConnectFourGroupManager


class TestThreatCombination(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_diagram_8_3(self):
        # This test is based on Diagram 8.3 from the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 1, ],
            ],
            [
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        self.env.player = 1

        pm = ConnectFourGroupManager(env_variables=self.env.env_variables)

        board = Board(self.env.env_variables)

        # This is the Even above Odd Threat combination described in Diagram 8.3.
        even_above_odd_tc = ThreatCombination(
            even_group=Group(player=0, start=Square(row=5, col=3), end=Square(row=2, col=6)),  # d1-g4,
            odd_group=Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6)),
            shared_square=Square(row=3, col=5),  # f3
            even_square=Square(row=2, col=6),  # g4
            odd_square=Square(row=3, col=6),  # g3
            directly_playable_square_shared_col=Square(row=5, col=5),  # f1
            directly_playable_square_stacked_col=Square(row=4, col=6),  # g2
            threat_combination_type=ThreatCombinationType.EvenAboveOdd,
        )
        # This is an Odd above not directly playable Even Threat Combination.
        # It wasn't talked about in the original paper for the related diagram, but it exists.
        odd_above_not_directly_playable_even_tc = ThreatCombination(
            even_group=Group(player=0, start=Square(row=1, col=1), end=Square(row=4, col=4)),  # b5-e2
            odd_group=Group(player=0, start=Square(row=1, col=1), end=Square(row=1, col=4)),  # b5-e5
            shared_square=Square(row=1, col=1),  # b5
            even_square=Square(row=2, col=2),  # c4
            odd_square=Square(row=1, col=2),  # c5
            directly_playable_square_shared_col=Square(row=5, col=1),  # b1
            directly_playable_square_stacked_col=Square(row=5, col=2),  # c2
            threat_combination_type=ThreatCombinationType.OddAboveNotDirectlyPlayableEven,
        )
        want_threat_combinations = {
            even_above_odd_tc,
            odd_above_not_directly_playable_even_tc,
        }
        got_threat_combinations = find_all_threat_combinations(board=board)
        self.assertEqual(want_threat_combinations, got_threat_combinations)

        want_even_above_odd_problems_solved = {
            # Solved by _no_odd_squares_in_crossing_column().
            Group(player=1, start=Square(row=0, col=5), end=Square(row=3, col=5)),  # f3-f6
            Group(player=1, start=Square(row=1, col=5), end=Square(row=4, col=5)),  # f2-f5
            Group(player=1, start=Square(row=2, col=5), end=Square(row=5, col=5)),  # f1-f4
            # Solved by _no_squares_above_crossing_and_above_odd().
            Group(player=1, start=Square(row=0, col=3), end=Square(row=0, col=6)),  # d6-g6
            Group(player=1, start=Square(row=2, col=3), end=Square(row=2, col=6)),  # d4-g4
            # Solved by _groups_containing_square_above_crossing_and_upper_stacked().
            # d4-g4 already included.
            # Solved by _highest_crossing_square_if_odd_is_playable().
            # None.
            # Solved by _threat_combination_baseinverse().
            # None.
            # Solved by _vertical_groups_in_stacked_column().
            Group(player=1, start=Square(row=0, col=6), end=Square(row=3, col=6)),  # g3-g6
            Group(player=1, start=Square(row=1, col=6), end=Square(row=4, col=6)),  # g2-g5
        }
        got_even_above_odd_problems_solved = even_above_odd_tc.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_even_above_odd_problems_solved, got_even_above_odd_problems_solved)

        want_odd_above_even_problems_solved = {
            # Solved by _no_odd_squares_in_crossing_column().
            Group(player=1, start=Square(row=0, col=1), end=Square(row=3, col=1)),  # b3-b6
            Group(player=1, start=Square(row=1, col=1), end=Square(row=4, col=1)),  # b2-b5
            Group(player=1, start=Square(row=2, col=1), end=Square(row=5, col=1)),  # b1-b4
            # Solved by _no_squares_above_crossing_and_above_odd().
            Group(player=1, start=Square(row=0, col=0), end=Square(row=0, col=3)),  # a6-d6
            Group(player=1, start=Square(row=0, col=1), end=Square(row=0, col=4)),  # b6-e6
            # Solved by _groups_containing_square_above_crossing_and_upper_stacked().
            # None.
            # Solved by _threat_combination_baseinverse().
            # None.
            # Solved by _vertical_groups_in_stacked_column().
            Group(player=1, start=Square(row=0, col=2), end=Square(row=3, col=2)),  # c3-c6
            Group(player=1, start=Square(row=1, col=2), end=Square(row=4, col=2)),  # c2-c5
            Group(player=1, start=Square(row=2, col=2), end=Square(row=5, col=2)),  # c1-c4
            Group(player=1, start=Square(row=0, col=2), end=Square(row=0, col=5)),  # c6-f6
        }
        got_odd_above_even_problems_solved = odd_above_not_directly_playable_even_tc.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_odd_above_even_problems_solved, got_odd_above_even_problems_solved)

    def test_diagram_8_7(self):
        # This test is a modification of Diagram 8.7 from the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
            ],
        ])
        pm = ConnectFourGroupManager(env_variables=self.env.env_variables)
        board = Board(self.env.env_variables)
        want_even_group = Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=6))  # d5-g2
        want_odd_group = Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6))  # d3-d3
        odd_above_directly_playable_even_threat_combination = ThreatCombination(
            even_group=want_even_group,
            odd_group=want_odd_group,
            shared_square=Square(row=3, col=5),  # f3
            even_square=Square(row=4, col=6),  # g2
            odd_square=Square(row=3, col=6),  # g3
            directly_playable_square_shared_col=Square(row=5, col=5),  # f1
            directly_playable_square_stacked_col=Square(row=4, col=6),  # g2
            threat_combination_type=ThreatCombinationType.OddAboveDirectlyPlayableEven,
        )
        want_threat_combinations = {
            odd_above_directly_playable_even_threat_combination,
        }
        got_threat_combinations = find_all_threat_combinations(board=board)
        self.assertEqual(want_threat_combinations, got_threat_combinations)

        want_problems_solved = {
            # Solved by _no_odd_squares_in_crossing_column().
            Group(player=1, start=Square(row=0, col=5), end=Square(row=3, col=5)),  # f3-f6
            Group(player=1, start=Square(row=1, col=5), end=Square(row=4, col=5)),  # f2-f5
            Group(player=1, start=Square(row=2, col=5), end=Square(row=5, col=5)),  # f1-f4
            # Solved by _no_squares_above_crossing_and_above_odd().
            Group(player=1, start=Square(row=0, col=3), end=Square(row=0, col=6)),  # d6-g6
            # Solved by _groups_containing_square_above_crossing_and_upper_stacked().
            Group(player=1, start=Square(row=0, col=3), end=Square(row=3, col=6)),  # d6-g3
            # Solved by _vertical_groups_in_stacked_column().
            Group(player=1, start=Square(row=0, col=6), end=Square(row=3, col=6)),  # g3-g6
            Group(player=1, start=Square(row=1, col=6), end=Square(row=4, col=6)),  # g2-g5
            Group(player=1, start=Square(row=2, col=6), end=Square(row=5, col=6)),  # g1-g4
        }
        got_problems_solved = odd_above_directly_playable_even_threat_combination.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_problems_solved, got_problems_solved)

    def test_exclude_directly_playable_shared_square(self):
        # If the crossing square is directly playable, the ThreatCombination should not be created.
        # Note that if a ThreatCombination using [(3,3)-(0,6)] and [(1,3)-(1,6)] cannot be created because
        # the shared square (1, 5) is directly playable.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 1, 0, 0, 1, 1, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 1, 1, 0, ],
                [0, 0, 1, 1, 0, 1, 0, ],
            ],
            [
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 0, 0, 1, 1, 0, ],
                [0, 1, 0, 1, 0, 0, 0, ],
                [1, 1, 0, 0, 1, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1
        board = Board(self.env.env_variables)
        got_threat_combinations = find_all_threat_combinations(board=board)
        self.assertFalse(got_threat_combinations)


if __name__ == '__main__':
    unittest.main()
