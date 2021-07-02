from typing import Set

from connect_four.evaluation.victor.solution.always_useful_fake_solution import AlwaysUsefulFakeSolution
from connect_four.problem.problem import Problem


class FakeSolution(AlwaysUsefulFakeSolution):
    def __init__(self, name: str,
                 solvable_problems: Set[Problem],
                 useful_problems: Set[Problem],
                 disallowed_solutions: Set[str]):
        super().__init__(name=name, solvable_problems=solvable_problems, disallowed_solutions=disallowed_solutions)
        self.useful_problems = useful_problems

    def is_useful(self, problems: Set[Problem]) -> bool:
        return not not self.useful_problems.intersection(problems)
