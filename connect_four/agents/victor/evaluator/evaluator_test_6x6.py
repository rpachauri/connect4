import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Threat
from connect_four.agents.victor.game.threat import create_square_to_threats

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Before

from connect_four.agents.victor.evaluator import solution
from connect_four.agents.victor.evaluator import evaluator

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestEvaluator6x6(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 6
        self.env.reset()

    def test_find_chosen_set_6x6(self):
        # This test case is based on the example given in Section 10.1.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        white_threats = board.potential_threats(0)
        square_to_threats = create_square_to_threats(threats=white_threats)

        # Define Rules that will be used as part of other Rules.
        claimeven_a1_a2 = Claimeven(lower=Square(row=5, col=0), upper=Square(row=4, col=0))
        claimeven_b1_b2 = Claimeven(lower=Square(row=5, col=1), upper=Square(row=4, col=1))
        vertical_c2_c3 = Vertical(lower=Square(row=4, col=2), upper=Square(row=3, col=2))
        vertical_d2_d3 = Vertical(lower=Square(row=4, col=3), upper=Square(row=3, col=3))
        claimeven_a3_a4 = Claimeven(lower=Square(row=3, col=0), upper=Square(row=2, col=0))
        claimeven_b3_b4 = Claimeven(lower=Square(row=3, col=1), upper=Square(row=2, col=1))
        vertical_c4_c5 = Vertical(lower=Square(row=2, col=2), upper=Square(row=1, col=2))
        vertical_d4_d5 = Vertical(lower=Square(row=2, col=3), upper=Square(row=1, col=3))
        claimeven_e1_e2 = Claimeven(lower=Square(row=5, col=4), upper=Square(row=4, col=4))
        claimeven_e3_e4 = Claimeven(lower=Square(row=3, col=4), upper=Square(row=2, col=4))
        claimeven_f1_f2 = Claimeven(lower=Square(row=5, col=5), upper=Square(row=4, col=5))
        claimeven_f3_f4 = Claimeven(lower=Square(row=3, col=5), upper=Square(row=2, col=5))

        # Define Rules that will be converted into Solutions.
        before_a1_a2_b1_b2_c2_c3_d2_d3 = solution.from_before(
            Before(
                threat=Threat(player=1, start=Square(row=4, col=0), end=Square(row=4, col=3)),  # a2-d2
                verticals=[vertical_c2_c3, vertical_d2_d3],
                claimevens=[claimeven_a1_a2, claimeven_b1_b2],
            ),
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(before_a1_a2_b1_b2_c2_c3_d2_d3)
        before_a3_a4_b3_b4_c4_c5_d4_d5 = solution.from_before(
            Before(
                threat=Threat(player=1, start=Square(row=2, col=0), end=Square(row=2, col=3)),  # a4-d4
                verticals=[vertical_c4_c5, vertical_d4_d5],
                claimevens=[claimeven_a3_a4, claimeven_b3_b4],
            ),
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(before_a3_a4_b3_b4_c4_c5_d4_d5)
        before_b1_b2_c2_c3_d2_d3_e1_e2 = solution.from_before(
            Before(
                threat=Threat(player=1, start=Square(row=4, col=1), end=Square(row=4, col=4)),  # b2-e2
                verticals=[vertical_c2_c3, vertical_d2_d3],
                claimevens=[claimeven_b1_b2, claimeven_e1_e2],
            ),
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(before_b1_b2_c2_c3_d2_d3_e1_e2)
        before_b3_b4_c4_c5_d4_d5_e3_e4 = solution.from_before(
            Before(
                threat=Threat(player=1, start=Square(row=2, col=1), end=Square(row=2, col=4)),  # b4-e4
                verticals=[vertical_c4_c5, vertical_d4_d5],
                claimevens=[claimeven_b3_b4, claimeven_e3_e4],
            ),
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(before_b3_b4_c4_c5_d4_d5_e3_e4)
        before_c2_c3_d2_d3_e1_e2_f1_f2 = solution.from_before(
            Before(
                threat=Threat(player=1, start=Square(row=4, col=2), end=Square(row=4, col=5)),  # c2-f2
                verticals=[vertical_c2_c3, vertical_d2_d3],
                claimevens=[claimeven_e1_e2, claimeven_f1_f2],
            ),
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(before_c2_c3_d2_d3_e1_e2_f1_f2)
        before_c4_c5_d4_d5_e3_e4_f3_f4 = solution.from_before(
            Before(
                threat=Threat(player=1, start=Square(row=2, col=2), end=Square(row=2, col=5)),  # c4-f4
                verticals=[vertical_c4_c5, vertical_d4_d5],
                claimevens=[claimeven_e3_e4, claimeven_f3_f4],
            ),
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(before_c4_c5_d4_d5_e3_e4_f3_f4)
        baseinverse_c1_d1 = solution.from_baseinverse(
            Baseinverse(
                playable1=Square(row=5, col=2),  # c1
                playable2=Square(row=5, col=3),  # d1
            ),
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(baseinverse_c1_d1)
        claimeven_a5_a6 = solution.from_claimeven(
            Claimeven(lower=Square(row=1, col=0), upper=Square(row=0, col=0)),
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(claimeven_a5_a6)
        claimeven_b5_b6 = solution.from_claimeven(
            Claimeven(lower=Square(row=1, col=1), upper=Square(row=0, col=1)),
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(claimeven_b5_b6)
        claimeven_e5_e6 = solution.from_claimeven(
            Claimeven(lower=Square(row=1, col=4), upper=Square(row=0, col=4)),
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(claimeven_e5_e6)
        claimeven_f5_f6 = solution.from_claimeven(
            Claimeven(lower=Square(row=1, col=5), upper=Square(row=0, col=5)),
            square_to_threats=square_to_threats,
        )
        self.assertIsNotNone(claimeven_f5_f6)

        # In this test case, the given Solution set is the desired set.
        solutions = {
            before_a1_a2_b1_b2_c2_c3_d2_d3,
            before_a3_a4_b3_b4_c4_c5_d4_d5,
            before_b1_b2_c2_c3_d2_d3_e1_e2,
            before_b3_b4_c4_c5_d4_d5_e3_e4,
            before_c2_c3_d2_d3_e1_e2_f1_f2,
            before_c4_c5_d4_d5_e3_e4_f3_f4,
            baseinverse_c1_d1,
            claimeven_a5_a6,
            claimeven_b5_b6,
            claimeven_e5_e6,
            claimeven_f5_f6,
        }
        node_graph = evaluator.create_node_graph(solutions=solutions)
        got_solutions = evaluator.find_chosen_set(
            node_graph=node_graph,
            problems=white_threats,
            allowed_solutions=solutions,
            used_solutions=set()
        )
        self.assertEqual(solutions, got_solutions)


if __name__ == '__main__':
    unittest.main()
