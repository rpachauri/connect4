from typing import Set

from connect_four.evaluation.victor.solution import SolutionManager
from connect_four.evaluation.victor.solution.solution2 import Solution
from connect_four.game import Square


class FakeSolutionManager(SolutionManager):
    def __init__(self, solutions: Set[Solution], win_conditions: Set[Solution] = None):
        self.solutions = solutions

        if win_conditions is None:
            win_conditions = set()
        self.win_conditions = win_conditions

    def move(self, player: int, row: int, col: int) -> Set[Square]:
        pass

    def undo_move(self):
        pass

    def get_solutions(self) -> Set[Solution]:
        return self.solutions

    def get_win_conditions(self) -> Set[Solution]:
        return self.win_conditions
