from typing import List, Set

from connect_four.game import Square
from connect_four.problem import Group as Problem
from connect_four.problem.problem_manager import ProblemManager


class FakeProblemManager(ProblemManager):
    def __init__(self, problems_by_square_by_player: List[List[List[Set[Problem]]]]):
        self.problems_by_square_by_player = problems_by_square_by_player

    def move(self, player: int, row: int, col: int) -> Set[Square]:
        pass

    def undo_move(self):
        pass

    def get_problems_by_square_by_player(self) -> List[List[List[Set[Problem]]]]:
        return self.problems_by_square_by_player

    def get_current_problems(self) -> Set[Problem]:
        pass

    def get_all_problems(self) -> Set[Problem]:
        pass
