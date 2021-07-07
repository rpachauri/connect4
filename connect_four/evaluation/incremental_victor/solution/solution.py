# So that we can use the Solution type within the Solution class.
from __future__ import annotations
from abc import abstractmethod
from enum import Enum
from typing import Set

from connect_four.problem.problem import Problem


class SolutionType(Enum):
    WHITE = 0
    BLACK = 1
    SHARED = 2


class Solution:
    def __init__(self, solution_type: SolutionType):
        self.solution_type = solution_type

    @abstractmethod
    def solves(self, problem: Problem) -> bool:
        pass

    @abstractmethod
    def is_useful(self, problems: Set[Problem]) -> bool:
        pass

    @abstractmethod
    def can_be_combined_with(self, solution: Solution) -> bool:
        pass
