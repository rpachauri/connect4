from typing import Set

from connect_four.evaluation.victor.solution.solution import Solution, SolutionType
from connect_four.problem.problem import Problem


class AlwaysUsefulFakeSolution(Solution):
    def __init__(self, name: str, solvable_problems: Set[Problem], disallowed_solutions: Set[str],
                 solution_type: SolutionType):
        super().__init__(solution_type=solution_type)
        self.name = name
        self.solvable_problems = solvable_problems
        self.disallowed_solutions = disallowed_solutions

    def solves(self, problem: Problem) -> bool:
        return problem in self.solvable_problems

    def is_useful(self, problems: Set[Problem]) -> bool:
        return True

    def can_be_combined_with(self, solution: Solution) -> bool:
        if isinstance(solution, AlwaysUsefulFakeSolution):
            return solution.name not in self.disallowed_solutions
        return False

    def __eq__(self, other):
        if isinstance(other, AlwaysUsefulFakeSolution):
            return self.name == other.name
        return False

    def __hash__(self):
        return self.name.__hash__()
