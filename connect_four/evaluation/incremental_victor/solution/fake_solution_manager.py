from typing import Set

from connect_four.evaluation.incremental_victor.solution.solution import Solution
from connect_four.evaluation.incremental_victor.solution.solution_manager import SolutionManager


class FakeSolutionManager(SolutionManager):
    def __init__(self, solutions: Set[Solution], win_conditions: Set[Solution] = None,
                 added_solutions: Set[Solution] = None, removed_solutions: Set[Solution] = None):
        self.solutions = solutions

        if win_conditions is None:
            win_conditions = set()
        self.win_conditions = win_conditions

        if added_solutions is None:
            added_solutions = set()
        self.added_solutions = added_solutions

        if removed_solutions is None:
            removed_solutions = set()
        self.removed_solutions = removed_solutions

    def move(self, player: int, row: int, col: int) -> (Set[Solution], Set[Solution]):
        return self.removed_solutions.copy(), self.added_solutions.copy()

    def undo_move(self) -> (Set[Solution], Set[Solution]):
        # The Solutions that were removed after a move are the ones that are added when undoing that move.
        return self.removed_solutions.copy(), self.added_solutions.copy()

    def get_solutions(self) -> Set[Solution]:
        return self.solutions

    def get_win_conditions(self) -> Set[Solution]:
        return self.win_conditions
