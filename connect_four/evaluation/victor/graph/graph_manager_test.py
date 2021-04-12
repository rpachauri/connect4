import unittest
from typing import List, Set

from connect_four.evaluation.victor.rules import Claimeven, Vertical
from connect_four.evaluation.victor.solution import solution2
from connect_four.game import Square
from connect_four.problem import Group as Problem
from connect_four.evaluation.victor.graph.graph_manager import GraphManager


class TestGraphManager(unittest.TestCase):

    @staticmethod
    def create_groups_by_square_by_player(
            num_rows: int, num_cols: int, problems: Set[Problem]) -> List[List[List[Set[Problem]]]]:
        groups_by_square_by_player = []
        for player in range(2):
            rows = []
            for row in range(num_rows):
                cols = []
                for col in range(num_cols):
                    cols.append(set())
                rows.append(cols)
            groups_by_square_by_player.append(rows)

        for problem in problems:
            for square in problem.squares:
                groups_by_square_by_player[problem.player][square.row][square.col].add(problem)
        return groups_by_square_by_player

    def test_create_node_graph(self):
        # Note that a Board is not required for create_node_graph().
        # Also note that the Solutions below are not exhaustive
        # (i.e. the Solutions could probably refute more groups),
        # but it is not necessary for the Solutions to be exhaustive for this test.

        problem_1 = Problem(player=0, start=Square(row=0, col=0), end=Square(row=3, col=3))  # a6-d3
        solution_1 = solution2.from_claimeven(claimeven=Claimeven(
            upper=Square(row=0, col=0),  # a6
            lower=Square(row=1, col=0),  # a5
        ))
        problem_2 = Problem(player=0, start=Square(row=1, col=0), end=Square(row=4, col=0))  # a5-a2
        solution_2 = solution2.from_vertical(vertical=Vertical(
            upper=Square(row=1, col=0),  # a5
            lower=Square(row=2, col=0),  # a4
        ))
        problem_3 = Problem(player=1, start=Square(row=0, col=1), end=Square(row=3, col=4))  # b6-e3
        solution_3 = solution2.from_claimeven(claimeven=Claimeven(
            upper=Square(row=0, col=1),  # b6
            lower=Square(row=1, col=1),  # b5
        ))
        want_problem_to_solutions = {
            problem_1: {solution_1},
            problem_2: {solution_2},
            problem_3: {solution_3},
        }
        want_solution_to_problems = {
            solution_1: {problem_1},
            solution_2: {problem_2},
            solution_3: {problem_3},
        }
        want_solution_to_solutions = {
            solution_1: {solution_1, solution_2},
            solution_2: {solution_1, solution_2},
            solution_3: {solution_3},
        }

        problems = {problem_1, problem_2, problem_3}
        groups_by_square_by_player = self.create_groups_by_square_by_player(num_rows=6, num_cols=7, problems=problems)
        got_problem_to_solutions, got_solution_to_problems, got_solution_to_solutions = GraphManager.create_node_graph(
            solutions={solution_1, solution_2, solution_3},
            groups_by_square_by_player=groups_by_square_by_player,
        )
        self.assertEqual(want_problem_to_solutions, got_problem_to_solutions)
        self.assertEqual(want_solution_to_problems, got_solution_to_problems)
        self.assertEqual(want_solution_to_solutions, got_solution_to_solutions)


if __name__ == '__main__':
    unittest.main()
