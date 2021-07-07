import gym
import unittest

import numpy as np

from connect_four.game import Square
from connect_four.problem import Group

from connect_four.evaluation.board import Board

from connect_four.evaluation.victor.rules import Claimeven
from connect_four.evaluation.victor.rules import Baseinverse

from connect_four.evaluation.victor.evaluator import evaluator
from connect_four.evaluation.victor.solution import solution1
from connect_four.evaluation.victor.threat_hunter import threat, threat_combination

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestEvaluator6x7(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_evaluate_6x7(self):
        # The empty 6x7 board has no solution set for Black because White is guaranteed to win.
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
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNone(got_evaluation)

    def test_evaluate_6x7_a1(self):
        # This test case is based on Appendix B: Situation after 1. a1.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [1, 0, 0, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_evaluation)

    def test_evaluate_6x7_b1(self):
        # This test case is based on Appendix B: Situation after 1. b1.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_evaluation)

    def test_evaluate_6x7_c1(self):
        # This test case is based on Appendix B: Situation after 1. c1.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_evaluation)

    def test_find_chosen_set_diagram_6_1(self):
        # This test case is based on Diagram 6.1.
        self.env.state = np.array([
            [
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        white_groups = board.potential_groups(0)
        square_to_groups = board.potential_groups_by_square()

        # Define all Solutions using Claimevens.
        # A subset of these Claimevens can refute all of white_groups.
        claimeven_a1_a2 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=0), upper=Square(row=4, col=0)),
            square_to_groups=square_to_groups,
        )
        claimeven_a3_a4 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=0), upper=Square(row=2, col=0)),
            square_to_groups=square_to_groups,
        )
        claimeven_a5_a6 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=0), upper=Square(row=0, col=0)),
            square_to_groups=square_to_groups,
        )
        claimeven_b1_b2 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=1), upper=Square(row=4, col=1)),
            square_to_groups=square_to_groups,
        )
        claimeven_b3_b4 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=1), upper=Square(row=2, col=1)),
            square_to_groups=square_to_groups,
        )
        claimeven_b5_b6 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=1), upper=Square(row=0, col=1)),
            square_to_groups=square_to_groups,
        )
        claimeven_c3_c4 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=2), upper=Square(row=2, col=2)),
            square_to_groups=square_to_groups,
        )
        claimeven_c5_c6 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=2), upper=Square(row=0, col=2)),
            square_to_groups=square_to_groups,
        )
        claimeven_e3_e4 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=4), upper=Square(row=2, col=4)),
            square_to_groups=square_to_groups,
        )
        claimeven_e5_e6 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=4), upper=Square(row=0, col=4)),
            square_to_groups=square_to_groups,
        )
        claimeven_f1_f2 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=5), upper=Square(row=4, col=5)),
            square_to_groups=square_to_groups,
        )
        claimeven_f3_f4 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=5), upper=Square(row=2, col=5)),
            square_to_groups=square_to_groups,
        )
        claimeven_f5_f6 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=5), upper=Square(row=0, col=5)),
            square_to_groups=square_to_groups,
        )
        claimeven_g1_g2 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=6), upper=Square(row=4, col=6)),
            square_to_groups=square_to_groups,
        )
        claimeven_g3_g4 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=6), upper=Square(row=2, col=6)),
            square_to_groups=square_to_groups,
        )
        claimeven_g5_g6 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=6), upper=Square(row=0, col=6)),
            square_to_groups=square_to_groups,
        )

        # Note that typically, for a given set of Solutions, there may be multiple subsets of Solutions that
        # solve all groups.
        # In this test case, the given Solution set is the desired set so there is exactly one subset.
        solutions = {
            claimeven_a1_a2,
            claimeven_a3_a4,
            claimeven_a5_a6,
            claimeven_b1_b2,
            claimeven_b3_b4,
            claimeven_b5_b6,
            claimeven_c3_c4,
            claimeven_c5_c6,
            claimeven_e3_e4,
            claimeven_e5_e6,
            claimeven_f1_f2,
            claimeven_f3_f4,
            claimeven_f5_f6,
            claimeven_g1_g2,
            claimeven_g3_g4,
            claimeven_g5_g6,
        }
        node_graph = evaluator.create_node_graph(solutions=solutions)
        got_solutions = evaluator.find_chosen_set(
            node_graph=node_graph,
            problems=white_groups,
            disallowed_solutions=set(),
            used_solutions=set()
        )
        self.assertIsNotNone(got_solutions)
        self.assertTrue(got_solutions.issubset(solutions))

        solved_groups = set()
        for sol in got_solutions:
            solved_groups.update(sol.groups)
        self.assertEqual(white_groups, solved_groups)

    def test_evaluate_6x7_8_1(self):
        # This test case is based on Diagram 8.1.
        # Black is to move and White has an odd threat at a3.
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
        self.env.player_turn = 1  # Black to move.
        board = Board(self.env.env_variables)
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_evaluation)

    def test_find_chosen_set_diagram_8_1(self):
        # This test case is based on Diagram 8.1.
        # Black is to move and White has an odd threat at a3.
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
        self.env.player_turn = 1  # Black to move.
        board = Board(self.env.env_variables)

        want_odd_threat_guarantor = threat.Threat(
            group=Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),
            empty_square=Square(row=3, col=0),
        )
        got_odd_threat_guarantor = evaluator.find_odd_threat_guarantor(board=board)
        self.assertEqual(want_odd_threat_guarantor, got_odd_threat_guarantor)

        square_to_groups = board.potential_groups_by_square()

        # Define all Solutions using Claimevens.
        # A subset of these Claimevens can refute all of Black's groups not in the 0th column.
        claimeven_b5_b6 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=1), upper=Square(row=0, col=1)),
            square_to_groups=square_to_groups,
        )
        claimeven_c5_c6 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=2), upper=Square(row=0, col=2)),
            square_to_groups=square_to_groups,
        )
        claimeven_f1_f2 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=5), upper=Square(row=4, col=5)),
            square_to_groups=square_to_groups,
        )
        claimeven_f3_f4 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=5), upper=Square(row=2, col=5)),
            square_to_groups=square_to_groups,
        )
        claimeven_f5_f6 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=5), upper=Square(row=0, col=5)),
            square_to_groups=square_to_groups,
        )
        claimeven_g3_g4 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=6), upper=Square(row=2, col=6)),
            square_to_groups=square_to_groups,
        )
        claimeven_g5_g6 = solution1.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=6), upper=Square(row=0, col=6)),
            square_to_groups=square_to_groups,
        )
        baseinverse_d5_e5 = solution1.from_baseinverse(
            baseinverse=Baseinverse(playable1=Square(row=1, col=3), playable2=Square(row=1, col=4)),
            square_to_groups=square_to_groups,
        )

        # Note that typically, for a given set of Solutions, there may be multiple subsets of Solutions that
        # solve all groups.
        # In this test case, the given Solution set is the desired set so there is exactly one subset.
        solutions = {
            claimeven_b5_b6,
            claimeven_c5_c6,
            claimeven_f1_f2,
            claimeven_f3_f4,
            claimeven_f5_f6,
            claimeven_g3_g4,
            claimeven_g5_g6,
            baseinverse_d5_e5,
        }

        black_groups = board.potential_groups(player=1)
        problems_solved_by_odd_threat = set()
        for row in range(want_odd_threat_guarantor.empty_square.row, 0, -1):
            square = Square(row=row, col=0)
            for problem in black_groups:
                if square in problem.squares:
                    problems_solved_by_odd_threat.add(problem)
        black_groups = black_groups - problems_solved_by_odd_threat

        node_graph = evaluator.create_node_graph(solutions=solutions)
        got_solutions = evaluator.find_chosen_set(
            node_graph=node_graph,
            problems=black_groups,
            disallowed_solutions=set(),
            used_solutions=set()
        )
        self.assertIsNotNone(got_solutions)
        self.assertTrue(got_solutions.issubset(solutions))

        solved_groups = set()
        for sol in got_solutions:
            solved_groups.update(sol.groups)
        self.assertEqual(black_groups, solved_groups)

    @unittest.skip("threat combination not yet implemented")
    def test_evaluate_6x7_even_above_odd_threat_combination(self):
        # This test case is based on Diagram 8.3.
        # Black is to move and White has a ThreatCombination at d1-g4 and d3-g3.
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
        self.env.player_turn = 1  # Black to move.
        board = Board(self.env.env_variables)
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_evaluation)

        want_odd_threat_guarantor = threat_combination.ThreatCombination(
            even_group=Group(player=0, start=Square(row=5, col=3), end=Square(row=2, col=6)),  # d1-g4
            odd_group=Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6)),  # d3-g3
            shared_square=Square(row=3, col=5),  # f3
            even_square=Square(row=2, col=6),  # g4
            odd_square=Square(row=3, col=6),  # g3
            threat_combination_type=threat_combination.ThreatCombinationType.EvenAboveOdd,
        )
        self.assertEqual(want_odd_threat_guarantor, got_evaluation.odd_threat_guarantor)

    @unittest.skip("threat combination not yet implemented")
    def test_evaluate_6x7_odd_above_not_directly_playable_even_threat_combination(self):
        # This test case is based on Diagram 8.7.
        # The even square of the ThreatCombination is NOT directly playable.
        # Black is to move and White has a ThreatCombination at d5-g2 and d3-g3.
        # Note that this test case is slightly modified. c2 and c3 were added because
        # c3-f6 cannot be refuted in Diagram 8.7.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 1, 0, 0, ],
                [0, 0, 1, 0, 1, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1  # Black to move.
        board = Board(self.env.env_variables)
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_evaluation)

        want_odd_threat_guarantor = threat_combination.ThreatCombination(
            even_group=Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=6)),  # d5-g2
            odd_group=Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6)),  # d3-g3
            shared_square=Square(row=3, col=5),  # f3
            even_square=Square(row=4, col=6),  # g2
            odd_square=Square(row=3, col=6),  # g3
            threat_combination_type=threat_combination.ThreatCombinationType.OddAboveNotDirectlyPlayableEven,
        )
        self.assertEqual(want_odd_threat_guarantor, got_evaluation.odd_threat_guarantor)

    @unittest.skip("threat combination not yet implemented")
    def test_evaluate_6x7_odd_above_directly_playable_even_threat_combination(self):
        # This test case is based on Diagram 8.7.
        # The even square of the ThreatCombination IS directly playable.
        # Black is to move and White has a ThreatCombination at d5-g2 and d3-g3.
        # Note that this test case is slightly modified. c2 and c3 were added because
        # c3-f6 cannot be refuted in Diagram 8.7.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 1, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 1, 0, 0, ],
                [0, 0, 1, 0, 1, 0, 1, ],
            ],
        ])
        self.env.player_turn = 1  # Black to move.
        board = Board(self.env.env_variables)
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_evaluation)

        want_odd_threat_guarantor = threat_combination.ThreatCombination(
            even_group=Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=6)),  # d5-g2
            odd_group=Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6)),  # d3-g3
            shared_square=Square(row=3, col=5),  # f3
            even_square=Square(row=4, col=6),  # g2
            odd_square=Square(row=3, col=6),  # g3
            threat_combination_type=threat_combination.ThreatCombinationType.OddAboveDirectlyPlayableEven,
        )
        self.assertEqual(want_odd_threat_guarantor, got_evaluation.odd_threat_guarantor)

    def test_evaluate_diagram_11_1_move_1(self):
        # This test case is based on Diagram 11.1, after White has played a1.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [1, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1  # Black to move.
        board = Board(self.env.env_variables)
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNone(got_evaluation)


if __name__ == '__main__':
    unittest.main()
