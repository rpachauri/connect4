from typing import Set

from connect_four.evaluation.victor.solution import SolutionManager
from connect_four.evaluation.victor.solution.solution2 import Solution
from connect_four.game import Square


class FakeSolutionManager(SolutionManager):
    def __init__(self, solutions: Set[Solution]):
        self.solutions = solutions

    def move(self, player: int, row: int, col: int) -> Set[Square]:
        pass

    def undo_move(self):
        pass

    def get_solutions(self) -> Set[Solution]:
        return self.solutions

    def get_win_conditions(self) -> Set[Solution]:
        pass
