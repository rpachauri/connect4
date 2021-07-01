import unittest

from connect_four.evaluation.victor.solution.fake_solution import FakeSolution
from connect_four.evaluation.victor.solution.fake_solution_manager import FakeSolutionManager
from connect_four.evaluation.victor.graph.graph_manager import GraphManager
from connect_four.problem.fake_problem import FakeProblem
from connect_four.problem.fake_problem_manager import FakeProblemManager


class TestGraphManager(unittest.TestCase):

    def test_create_node_graph(self):
        problem_1 = FakeProblem(name="p1")
        problem_2 = FakeProblem(name="p2")
        problem_3 = FakeProblem(name="p3")
        solution_1 = FakeSolution(
            name="s1",
            solvable_problems={problem_1},
            disallowed_solutions={"s1", "s2"},
        )
        solution_2 = FakeSolution(
            name="s2",
            solvable_problems={problem_2},
            disallowed_solutions={"s1", "s2"},
        )
        solution_3 = FakeSolution(
            name="s3",
            solvable_problems={problem_3},
            disallowed_solutions={"s3"},
        )

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

        fake_problem_manager = FakeProblemManager(problems={problem_1, problem_2, problem_3})
        fake_solution_manager = FakeSolutionManager(solutions={solution_1, solution_2, solution_3})

        gm = GraphManager(player=0, problem_manager=fake_problem_manager, solution_manager=fake_solution_manager)
        self.assertEqual(want_problem_to_solutions, gm.problem_to_solutions)
        self.assertEqual(want_solution_to_problems, gm.solution_to_problems)
        self.assertEqual(want_solution_to_solutions, gm.solution_to_solutions)


if __name__ == '__main__':
    unittest.main()
