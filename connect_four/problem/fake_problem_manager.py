from typing import Set, List

from connect_four.game import Square
from connect_four.problem.problem import Problem
from connect_four.problem.problem_manager import ProblemManager


class FakeProblemManager(ProblemManager):
    def __init__(self, problems: Set[Problem], removed_problems: Set[Problem] = None):
        self.problems = problems
        self.removed_problems = removed_problems

    def move(self, player: int, row: int, col: int) -> (Set[Square], Set[Problem]):
        return None, self.removed_problems.copy()

    def undo_move(self) -> Set[Problem]:
        return self.removed_problems.copy()

    def get_problems_by_square_by_player(self) -> List[List[List[Set[Problem]]]]:
        pass

    def get_current_problems(self) -> Set[Problem]:
        pass

    def get_all_problems(self) -> Set[Problem]:
        return self.problems.copy()
