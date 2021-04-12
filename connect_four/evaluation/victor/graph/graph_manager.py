from typing import Set, Dict

from connect_four.evaluation.victor.solution import SolutionManager
from connect_four.problem import Group as Problem
from connect_four.evaluation.victor.solution import combination
from connect_four.evaluation.victor.solution.solution2 import Solution
from connect_four.problem.problem_manager import ProblemManager


class GraphManager:
    def __init__(self, player: int,
                 problem_manager: ProblemManager,
                 solution_manager: SolutionManager):
        """Initializes the SolutionManager with the given env_variables.

        Args:
            player (int): the current player.
            problem_manager (ProblemManager): a ProblemManager whose internal state matches env_variables.
            solution_manager (SolutionManager): a SolutionManager whose internal state matches env_variables.
        """
        self.player = player
        self.problem_manager = problem_manager
        self.solution_manager = solution_manager

        self._initialize_node_graph()

    def _initialize_node_graph(self):
        """Initializes the NodeGraph connecting Problems to Solutions, Solutions to Problems, and Solutions to Solutions.
        """
        solutions = self.solution_manager.get_solutions()
        problems_by_square_by_player = self.problem_manager.get_problems_by_square_by_player()

        self.problem_to_solutions: Dict[Problem, Set[Solution]] = {}
        self.solution_to_problems: Dict[Solution, Set[Problem]] = {}
        self.solution_to_solutions: Dict[Solution, Set[Solution]] = {}

        for solution in solutions:
            problems_solved = solution.rule_instance.find_problems_solved(
                groups_by_square_by_player=problems_by_square_by_player,
            )

            self.solution_to_problems[solution] = set()
            for problem in problems_solved:
                if problem not in self.problem_to_solutions:
                    self.problem_to_solutions[problem] = set()
                self.problem_to_solutions[problem].add(solution)
                self.solution_to_problems[solution].add(problem)

            self.solution_to_solutions[solution] = set()
            for other in solutions:
                if not combination.allowed(s1=solution, s2=other):
                    self.solution_to_solutions[solution].add(other)

    def move(self, row: int, col: int):
        """Plays a move at the given row and column for the current player.

        Assumptions:
            1.  The internal state of the GraphManager is not at a terminal state.

        Args:
            row (int): the row to play
            col (int): the column to play

        Returns:
            Nothing.
        """
        pass

    def undo_move(self):
        """Undoes the most recent move.

        Raises:
            (AssertionError): if the internal state of the GraphManager is at the state given upon initialization.
        """
        pass

    def evaluate(self) -> Set[Solution]:
        """Evaluates the current position.

        Returns:
            chosen_set (Set[Solution]): A set of Solutions that solves the current state.
                                        None if no such set can be found for the current position.

            Implications of chosen_set depending on the current player:
            1. If chosen_set is None:
                No guarantees can be made on the game-theoretic value of the current position.
            2. Else if the current player is White:
                Black can guarantee at least a draw.
            3. Else: # the current player is Black:
                White can guarantee a win.
        """
        problems = self._get_current_problems()
        return self._find_chosen_set(problems=problems, disallowed_solutions=set(), used_solutions=set())

    def _get_current_problems(self) -> Set[Problem]:
        """
        Returns:
            current_problems (Set[Problem]): a subset of the Problems in this node graph that
                belong to the current player.
        """
        current_problems = set()
        for problem in self.problem_to_solutions:
            if problem.player == self.player:
                current_problems.add(problem)
        return current_problems

    def _find_chosen_set(self,
                         problems: Set[Problem],
                         disallowed_solutions: Set[Solution],
                         used_solutions: Set[Solution]) -> Set[Solution]:
        """Finds a "chosen set" of Solutions that can be used to solve problems.

        Args:
            problems (Set[Problem]): a set of Problems to solve.
            disallowed_solutions (Set[Solution]): a set of Solutions that cannot be used.
            used_solutions (Set[Solution]): a set of Solutions that are already in use.

        Returns:
            chosen_set (Set[Solution]):
                If problems is empty, a copy of used_solutions.
                Else if problems is solvable without the use of disallowed_solutions, a superset of used_solutions.
                Else: None.
        """
        # Base Case.
        if not problems:
            # If there are no unsolved problems, return the set of Solutions currently in use.
            return used_solutions.copy()

        # Recursive Case.
        # Find the most difficult problem to solve.
        most_difficult_problem = self._problem_with_fewest_solutions(
            problems=problems, disallowed_solutions=disallowed_solutions)
        # Find all solutions that can be used to solve the most difficult problem.
        most_difficult_problem_usable_solutions = self.problem_to_solutions[most_difficult_problem].difference(
            disallowed_solutions)

        for solution in most_difficult_problem_usable_solutions:
            # Choose.
            used_solutions.add(solution)
            # Recurse.
            chosen_set = self._find_chosen_set(
                problems=problems - self.solution_to_problems[solution],
                disallowed_solutions=disallowed_solutions.union(self.solution_to_solutions[solution]),
                used_solutions=used_solutions,
            )
            # Unchoose.
            used_solutions.remove(solution)

            if chosen_set is not None:
                return chosen_set

    def _problem_with_fewest_solutions(self, problems: Set[Problem], disallowed_solutions: Set[Solution]) -> Problem:
        """Finds the problem with the fewest allowed Solutions.

        Args:
            problems (Set[Problem]): a set of Problems to solve.
            disallowed_solutions (Set[Solution]): a set of Solutions that cannot be used.

        Returns:
            most_difficult_problem (Problem): the Problem with the fewest allowed Solutions.
        """
        most_difficult_problem = None
        num_neighbors_of_most_difficult = len(self.solution_to_problems) + 1  # Set to an arbitrary high number.

        # Find the Problem in problems with the fewest solutions in this graph.
        # Exclude any Solution in disallowed_solutions.
        for problem in problems:
            num_nodes = len(self.problem_to_solutions[problem].difference(disallowed_solutions))
            if num_nodes < num_neighbors_of_most_difficult:
                most_difficult_problem = problem
                num_neighbors_of_most_difficult = num_nodes

        # If we didn't find a most_difficult_problem, then that means there isn't a single Problem in both
        # problems and node_graph.
        if most_difficult_problem is not None:
            return most_difficult_problem

        raise ValueError("No problem in problems and node_graph")
