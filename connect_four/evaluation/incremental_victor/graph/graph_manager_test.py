import unittest

from connect_four.evaluation.incremental_victor.solution.always_useful_fake_solution import AlwaysUsefulFakeSolution
from connect_four.evaluation.incremental_victor.solution.fake_solution import FakeSolution
from connect_four.evaluation.incremental_victor.solution.fake_solution_manager import FakeSolutionManager
from connect_four.evaluation.incremental_victor.graph.graph_manager import GraphManager
from connect_four.evaluation.incremental_victor.solution.solution import SolutionType
from connect_four.problem.fake_problem import FakeProblem
from connect_four.problem.fake_problem_manager import FakeProblemManager


@unittest.skip("deprecated")
class TestGraphManager(unittest.TestCase):

    def test_create_node_graph(self):
        problem_1 = FakeProblem(name="p1")
        problem_2 = FakeProblem(name="p2")
        problem_3 = FakeProblem(name="p3")
        solution_1 = AlwaysUsefulFakeSolution(
            name="s1",
            solvable_problems={problem_1},
            disallowed_solutions={"s1", "s2"},
        )
        solution_2 = AlwaysUsefulFakeSolution(
            name="s2",
            solvable_problems={problem_2},
            disallowed_solutions={"s1", "s2"},
        )
        solution_3 = AlwaysUsefulFakeSolution(
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

    def test_create_node_graph_with_useless_solution(self):
        problem_1 = FakeProblem(name="p1")
        # We will not be giving problem_2 to the ProblemManager.
        problem_2 = FakeProblem(name="p2")
        solution_1 = FakeSolution(
            name="s1",
            solvable_problems={problem_1},
            useful_problems={problem_1},
            disallowed_solutions={"s1", "s2"},
        )
        # Even though solution_2 can solve problem_1, since problem_2 is the only problem that makes solution_2 useful,
        # if problem_2 is not in the Graph, solution_2 should be pruned.
        solution_2 = FakeSolution(
            name="s2",
            solvable_problems={problem_1, problem_2},
            useful_problems={problem_2},
            disallowed_solutions={"s1", "s2"},
        )

        want_problem_to_solutions = {
            problem_1: {solution_1},
        }
        want_solution_to_problems = {
            solution_1: {problem_1},
        }
        want_solution_to_solutions = {
            solution_1: {solution_1},
        }

        fake_problem_manager = FakeProblemManager(problems={problem_1})
        fake_solution_manager = FakeSolutionManager(solutions={solution_1, solution_2})

        gm = GraphManager(player=0, problem_manager=fake_problem_manager, solution_manager=fake_solution_manager)
        self.assertEqual(want_problem_to_solutions, gm.problem_to_solutions)
        self.assertEqual(want_solution_to_problems, gm.solution_to_problems)
        self.assertEqual(want_solution_to_solutions, gm.solution_to_solutions)

    def test_move_add_solution(self):
        problem_1 = FakeProblem(name="p1")
        solution_1 = AlwaysUsefulFakeSolution(
            name="s1",
            solvable_problems={problem_1},
            disallowed_solutions={"s1"},
        )

        fake_problem_manager = FakeProblemManager(problems={problem_1}, removed_problems=set())
        fake_solution_manager = FakeSolutionManager(
            solutions=set(),
            removed_solutions=set(),
            added_solutions={solution_1},
        )

        # Upon initialization, there is only 1 Problem in the Graph - no Solutions.
        gm = GraphManager(player=0, problem_manager=fake_problem_manager, solution_manager=fake_solution_manager)
        want_problem_to_solutions = {
            problem_1: set(),
        }
        self.assertEqual(want_problem_to_solutions, gm.problem_to_solutions)
        self.assertFalse(gm.solution_to_problems)
        self.assertFalse(gm.solution_to_solutions)

        # After moving, there is now one Solution in the Graph.
        gm.move(row=0, col=0)
        want_problem_to_solutions = {
            problem_1: {solution_1},
        }
        want_solution_to_problems = {
            solution_1: {problem_1},
        }
        want_solution_to_solutions = {
            solution_1: {solution_1},
        }
        self.assertEqual(want_problem_to_solutions, gm.problem_to_solutions)
        self.assertEqual(want_solution_to_problems, gm.solution_to_problems)
        self.assertEqual(want_solution_to_solutions, gm.solution_to_solutions)

    def test_move_remove_solution(self):
        problem_1 = FakeProblem(name="p1")
        solution_1 = AlwaysUsefulFakeSolution(
            name="s1",
            solvable_problems={problem_1},
            disallowed_solutions={"s1"},
        )

        fake_problem_manager = FakeProblemManager(problems={problem_1}, removed_problems=set())
        fake_solution_manager = FakeSolutionManager(
            solutions={solution_1},
            removed_solutions={solution_1},
            added_solutions=set(),
        )

        # Upon initialization, there is only 1 Problem in the Graph - no Solutions.
        gm = GraphManager(player=0, problem_manager=fake_problem_manager, solution_manager=fake_solution_manager)
        want_problem_to_solutions = {
            problem_1: {solution_1},
        }
        want_solution_to_problems = {
            solution_1: {problem_1},
        }
        want_solution_to_solutions = {
            solution_1: {solution_1},
        }
        self.assertEqual(want_problem_to_solutions, gm.problem_to_solutions)
        self.assertEqual(want_solution_to_problems, gm.solution_to_problems)
        self.assertEqual(want_solution_to_solutions, gm.solution_to_solutions)

        # After moving, there is now one Solution in the Graph.
        gm.move(row=0, col=0)
        want_problem_to_solutions = {
            problem_1: set(),
        }
        self.assertEqual(want_problem_to_solutions, gm.problem_to_solutions)
        self.assertFalse(gm.solution_to_problems)
        self.assertFalse(gm.solution_to_solutions)

    def test_remove_nonexistent_solution(self):
        solution_1 = AlwaysUsefulFakeSolution(
            name="s1",
            solvable_problems=set(),
            disallowed_solutions={"s1"},
        )

        # Initialize an empty Graph.
        fake_problem_manager = FakeProblemManager(problems=set())
        fake_solution_manager = FakeSolutionManager(solutions=set())
        gm = GraphManager(player=0, problem_manager=fake_problem_manager, solution_manager=fake_solution_manager)

        # Attempt to remove a Solution that is not even in the Graph. There should be no issue.
        gm._remove_solution(solution=solution_1)

        self.assertFalse(gm.problem_to_solutions)
        self.assertFalse(gm.solution_to_problems)
        self.assertFalse(gm.solution_to_solutions)

    def test_add_white_solution(self):
        problem_1 = FakeProblem(name="p1")
        white_solution = AlwaysUsefulFakeSolution(
            name="s1",
            solvable_problems={problem_1},
            disallowed_solutions={"s1"},
            solution_type=SolutionType.WHITE,
        )

        fake_problem_manager = FakeProblemManager(problems={problem_1}, removed_problems=set())
        fake_solution_manager = FakeSolutionManager(
            solutions={white_solution},
            removed_solutions=set(),
            added_solutions=set(),
        )

        # Upon initialization, there is only 1 Problem in the Graph - no Solutions.
        gm = GraphManager(player=0, problem_manager=fake_problem_manager, solution_manager=fake_solution_manager)
        self.assertEqual({white_solution}, gm.white_solutions)

    def test_white_separate_from_black(self):
        # Create a Graph with 1 White Solution and 1 Black Solution.
        white_solution = AlwaysUsefulFakeSolution(
            name="white",
            solvable_problems=set(),
            disallowed_solutions={"white", "black"},
            solution_type=SolutionType.WHITE,
        )
        black_solution = AlwaysUsefulFakeSolution(
            name="black",
            solvable_problems=set(),
            disallowed_solutions={"white", "black"},
            solution_type=SolutionType.BLACK,
        )

        fake_problem_manager = FakeProblemManager(problems=set(), removed_problems=set())
        fake_solution_manager = FakeSolutionManager(
            solutions={white_solution, black_solution},
            removed_solutions=set(),
            added_solutions=set(),
        )

        gm = GraphManager(player=0, problem_manager=fake_problem_manager, solution_manager=fake_solution_manager)
        self.assertEqual({white_solution}, gm.white_solutions)
        self.assertEqual({black_solution}, gm.black_solutions)
        self.assertFalse(gm.shared_solutions)
        want_solution_to_problems = {
            white_solution: set(),
            black_solution: set(),
        }
        # Even though white_solution cannot be combined with black_solution, they are not connected to each other.
        want_solution_to_solutions = {
            white_solution: {white_solution},
            black_solution: {black_solution},
        }
        self.assertEqual(want_solution_to_problems, gm.solution_to_problems)
        self.assertEqual(want_solution_to_solutions, gm.solution_to_solutions)


if __name__ == '__main__':
    unittest.main()
