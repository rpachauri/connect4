import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Threat

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor import Before
from connect_four.agents.victor import find_all_befores
from connect_four.agents.victor.rules.before import add_before_variations
from connect_four.agents.victor.rules.before import empty_squares_of_before_group

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestBefore(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_before(self):
        self.env.state = np.array([
            [
                [0, 0, 1, 0, 0, 0, 1, ],
                [1, 1, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [1, 1, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [1, 1, 0, 1, 1, 0, 1, ],
            ],
            [
                [1, 1, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [1, 1, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [1, 1, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        # With White to move, every Before group must belong to Black.
        black_threats = board.potential_threats(1)
        got_befores = find_all_befores(board, black_threats)

        threat_4_3_to_4_6 = Threat(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6))
        threat_2_3_to_2_6 = Threat(player=1, start=Square(row=2, col=3), end=Square(row=2, col=6))
        threat_1_3_to_4_6 = Threat(player=1, start=Square(row=1, col=3), end=Square(row=4, col=6))
        threat_0_5_to_3_5 = Threat(player=1, start=Square(row=0, col=5), end=Square(row=3, col=5))
        threat_1_5_to_4_5 = Threat(player=1, start=Square(row=1, col=5), end=Square(row=4, col=5))
        threat_2_5_to_5_5 = Threat(player=1, start=Square(row=2, col=5), end=Square(row=5, col=5))
        want_threats = {
            threat_4_3_to_4_6,
            threat_2_3_to_2_6,
            threat_1_3_to_4_6,
            threat_0_5_to_3_5,
            threat_1_5_to_4_5,
            threat_2_5_to_5_5,
        }
        self.assertEqual(want_threats, black_threats)

        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        vertical_1_5 = Vertical(upper=Square(row=1, col=5), lower=Square(row=2, col=5))
        vertical_2_5 = Vertical(upper=Square(row=2, col=5), lower=Square(row=3, col=5))

        want_befores = {
            Before(threat=threat_4_3_to_4_6, verticals=[vertical_3_5], claimevens=[]),
            Before(threat=threat_2_3_to_2_6, verticals=[vertical_1_5], claimevens=[]),
            # The Before below is excluded because it doesn't have any verticals. This makes it an Aftereven.
            # claimeven_3_5 = Claimeven(upper=Square(row=2, col=5), lower=Square(row=3, col=5))
            # Before(threat=threat_2_3_to_2_6, verticals=[], claimevens=[claimeven_3_5]),
            Before(threat=threat_1_3_to_4_6, verticals=[vertical_3_5], claimevens=[]),
            Before(threat=threat_1_3_to_4_6, verticals=[vertical_2_5], claimevens=[]),
        }
        self.assertEqual(want_befores, got_befores)

    def test_add_before_variations_diagram_6_8(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 1, ],
                [0, 0, 1, 0, 0, 1, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        threat_4_3_to_4_6 = Threat(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6))

        befores = set()
        add_before_variations(board=board,
                              befores=befores,
                              threat=threat_4_3_to_4_6,
                              empty_squares=[Square(row=4, col=5)],
                              verticals=[],
                              claimevens=[])
        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        want_befores = {
            Before(threat=threat_4_3_to_4_6, verticals=[vertical_3_5], claimevens=[]),
        }
        self.assertEqual(want_befores, befores)

    def test_add_before_variations_diagram_6_9(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        threat_2_1_to_5_4 = Threat(player=1, start=Square(row=2, col=1), end=Square(row=5, col=4))

        befores = set()
        add_before_variations(board=board,
                              befores=befores,
                              threat=threat_2_1_to_5_4,
                              empty_squares=[Square(row=2, col=1), Square(row=5, col=4)],
                              verticals=[],
                              claimevens=[])
        vertical_1_1 = Vertical(upper=Square(row=1, col=1), lower=Square(row=2, col=1))
        claimeven_2_1 = Claimeven(upper=Square(row=2, col=1), lower=Square(row=3, col=1))
        vertical_4_4 = Vertical(upper=Square(row=4, col=4), lower=Square(row=5, col=4))
        want_befores = {
            Before(threat=threat_2_1_to_5_4, verticals=[vertical_1_1, vertical_4_4], claimevens=[]),
            Before(threat=threat_2_1_to_5_4, verticals=[vertical_4_4], claimevens=[claimeven_2_1]),
        }
        self.assertEqual(want_befores, befores)

    def test_add_before_variations_diagram_6_10(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        threat_4_3_to_4_6 = Threat(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6))

        befores = set()
        add_before_variations(board=board,
                              befores=befores,
                              threat=threat_4_3_to_4_6,
                              empty_squares=[Square(row=4, col=4), Square(row=4, col=5), Square(row=4, col=6)],
                              verticals=[],
                              claimevens=[])
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))
        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        claimeven_4_5 = Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5))
        vertical_3_6 = Vertical(upper=Square(row=3, col=6), lower=Square(row=4, col=6))
        claimeven_4_6 = Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6))
        want_befores = {
            Before(threat=threat_4_3_to_4_6, verticals=[vertical_3_4, vertical_3_5, vertical_3_6], claimevens=[]),
            Before(threat=threat_4_3_to_4_6, verticals=[vertical_3_4, vertical_3_5], claimevens=[claimeven_4_6]),
            Before(threat=threat_4_3_to_4_6, verticals=[vertical_3_4, vertical_3_6], claimevens=[claimeven_4_5]),
            Before(threat=threat_4_3_to_4_6, verticals=[vertical_3_4], claimevens=[claimeven_4_5, claimeven_4_6]),
        }
        self.assertEqual(want_befores, befores)

        want_empty_squares = frozenset([Square(row=4, col=4), Square(row=4, col=5), Square(row=4, col=6)])
        for b in befores:
            self.assertSetEqual(want_empty_squares, b.empty_squares_of_before_group())

    def test_empty_squares_of_before_group_diagram_6_10(self):
        # Note that this tests the function empty_squares_of_before_group.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        threat_4_3_to_4_6 = Threat(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6))
        want_empty_squares = [Square(row=4, col=4), Square(row=4, col=5), Square(row=4, col=6)]

        got_empty_squares = empty_squares_of_before_group(board=board, threat=threat_4_3_to_4_6)
        self.assertCountEqual(want_empty_squares, got_empty_squares)


if __name__ == '__main__':
    unittest.main()
