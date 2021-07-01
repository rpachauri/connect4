from typing import Set

from connect_four.evaluation.victor.solution.solution import Solution
from connect_four.problem.problem import Problem


class FakeSolution(Solution):
    def __init__(self, name: str, solvable_problems: Set[Problem], disallowed_solutions: Set[str]):
        self.name = name
        self.solvable_problems = solvable_problems
        self.disallowed_solutions = disallowed_solutions

    def solves(self, problem: Problem) -> bool:
        return problem in self.solvable_problems

    def is_useful(self, problems: Set[Problem]) -> bool:
        return True

    def can_be_combined_with(self, solution: Solution) -> bool:
        if isinstance(solution, FakeSolution):
            return solution.name not in self.disallowed_solutions
        return False

    def __eq__(self, other):
        if isinstance(other, FakeSolution):
            return self.name == other.name
        return False

    def __hash__(self):
        return self.name.__hash__()
