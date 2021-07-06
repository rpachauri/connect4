from typing import Set, Dict

from connect_four.evaluation.victor.solution import SolutionManager
from connect_four.evaluation.victor.solution.solution import Solution, SolutionType
from connect_four.problem.problem import Problem
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
        """Initializes the NodeGraph connecting Problems to Solutions,
        Solutions to Problems, and Solutions to Solutions.
        """
        self.problem_to_solutions: Dict[Problem, Set[Solution]] = {}
        self.solution_to_problems: Dict[Solution, Set[Problem]] = {}
        self.solution_to_solutions: Dict[Solution, Set[Solution]] = {}
        self.solutions_removed_by_move = []
        # Keep track of useful Solutions by type.
        self.white_solutions = set()
        self.black_solutions = set()
        self.shared_solutions = set()

        problems = self.problem_manager.get_all_problems()
        solutions = self.solution_manager.get_solutions()

        for problem in problems:
            self._add_problem(problem)

        for solution in solutions:
            self._add_solution(solution)

        print("number of useful solutions =", len(self.solution_to_solutions))

    def _add_problem(self, problem: Problem):
        """Adds a Problem to this Graph.

        Args:
            problem (Problem): a Problem to add to this Graph.

        Returns:
            None.
        """
        self._representational_invariant()

        self.problem_to_solutions[problem] = set()
        for solution in self.solution_to_problems:
            if solution.solves(problem=problem):
                self.solution_to_problems[solution].add(problem)
                self.problem_to_solutions[problem].add(solution)

        self._representational_invariant()

    def _add_solution(self, solution: Solution):
        """Adds a Solution to this Graph if it is useful.

        Requires:
            1. All Problems in the current state should be added to this Graph.

        Args:
            solution (Solution): a Solution to add to this Graph.

        Returns:
            None.
        """
        self._representational_invariant()

        solved_problems = set()
        for problem in self.problem_to_solutions:
            if solution.solves(problem=problem):
                solved_problems.add(problem)

        # Don't add the Solution to this Graph if it is not useful.
        if not solution.is_useful(problems=solved_problems):
            return

        # Now that we know the Solution is useful, we add it to the Graph.
        for problem in solved_problems:
            self.problem_to_solutions[problem].add(solution)

        self.solution_to_problems[solution] = solved_problems

        if solution.solution_type == SolutionType.WHITE:
            self._add_white_solution(solution=solution)
        elif solution.solution_type == SolutionType.BLACK:
            self._add_black_solution(solution=solution)
        else:  # solution.type == SolutionType.Shared
            self._add_shared_solution(solution=solution)

        self._representational_invariant()

    def _add_white_solution(self, solution: Solution):
        self.white_solutions.add(solution)
        self.solution_to_solutions[solution] = set()
        for other_solution in self.white_solutions:
            if not solution.can_be_combined_with(solution=other_solution):
                self.solution_to_solutions[solution].add(other_solution)
                self.solution_to_solutions[other_solution].add(solution)
        for other_solution in self.shared_solutions:
            if not solution.can_be_combined_with(solution=other_solution):
                self.solution_to_solutions[solution].add(other_solution)
                self.solution_to_solutions[other_solution].add(solution)

    def _add_black_solution(self, solution: Solution):
        self.black_solutions.add(solution)
        self.solution_to_solutions[solution] = set()
        for other_solution in self.black_solutions:
            if not solution.can_be_combined_with(solution=other_solution):
                self.solution_to_solutions[solution].add(other_solution)
                self.solution_to_solutions[other_solution].add(solution)
        for other_solution in self.shared_solutions:
            if not solution.can_be_combined_with(solution=other_solution):
                self.solution_to_solutions[solution].add(other_solution)
                self.solution_to_solutions[other_solution].add(solution)

    def _add_shared_solution(self, solution: Solution):
        self.shared_solutions.add(solution)
        self.solution_to_solutions[solution] = set()
        for other_solution in self.solution_to_solutions:
            if not solution.can_be_combined_with(solution=other_solution):
                self.solution_to_solutions[solution].add(other_solution)
                self.solution_to_solutions[other_solution].add(solution)

    def _remove_problem(self, problem: Problem):
        """Removes a Problem from this Graph.
        If any affected Solutions become no longer useful, prunes those Solutions from the Graph.

        Args:
            problem (Problem): a Problem to remove.

        Returns:
            None.
        """
        self._representational_invariant()

        affected_solutions = self.problem_to_solutions.pop(problem)
        for solution in affected_solutions:
            self.solution_to_problems[solution].remove(problem)

        for solution in affected_solutions:
            if not solution.is_useful(self.solution_to_problems[solution]):
                self._remove_solution(solution=solution)
                self.solutions_removed_by_move[-1].add(solution)

        self._representational_invariant()

    def _remove_solution(self, solution: Solution):
        """Removes a Solution from this Graph.

        Args:
            solution (Solution): a Solution to remove.

        Returns:
            None.
        """
        self._representational_invariant()

        if solution not in self.solution_to_solutions:
            return None

        if solution.solution_type == SolutionType.WHITE:
            self.white_solutions.remove(solution)
        elif solution.solution_type == SolutionType.BLACK:
            self.black_solutions.remove(solution)
        else:  # solution.solution_type == SolutionType.SHARED
            self.shared_solutions.remove(solution)

        affected_solutions = self.solution_to_solutions.pop(solution)
        for other_solution in affected_solutions:
            if other_solution != solution:
                self.solution_to_solutions[other_solution].remove(solution)

        affected_problems = self.solution_to_problems.pop(solution)
        for problem in affected_problems:
            self.problem_to_solutions[problem].remove(solution)

        self._representational_invariant()

    def _representational_invariant(self):
        # # The key set of solution_to_problems should equal solution_to_solutions.
        # assert self.solution_to_problems.keys() == self.solution_to_solutions.keys()
        #
        # # The three Solution Sets should equal the key set of the above two Dicts.
        # assert (self.white_solutions.union(self.black_solutions).union(self.shared_solutions) ==
        #         self.solution_to_solutions.keys())
        #
        # # The three Solution sets should be disjoint.
        # assert self.white_solutions.isdisjoint(self.black_solutions)
        # assert self.white_solutions.isdisjoint(self.shared_solutions)
        # assert self.black_solutions.isdisjoint(self.shared_solutions)
        #
        # # Every Solution in the Graph should be useful.
        # for solution in self.solution_to_problems:
        #     assert solution.is_useful(self.solution_to_problems[solution])
        #
        # # Every Solution in the Graph should be a key in solution_to_solutions.
        # for solution in self.solution_to_solutions:
        #     assert self.solution_to_solutions[solution].issubset(self.solution_to_solutions.keys())
        pass

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
        self.solutions_removed_by_move.append(set())
        _, removed_problems = self.problem_manager.move(player=self.player, row=row, col=col)
        for problem in removed_problems:
            self._remove_problem(problem=problem)

        removed_solutions, added_solutions = self.solution_manager.move(player=self.player, row=row, col=col)
        print("len(removed_solutions) = ", len(removed_solutions))
        print("len(added_solutions) = ", len(added_solutions))
        print("number of useful solutions =", len(self.solution_to_solutions))
        for solution in removed_solutions:
            self._remove_solution(solution=solution)
        print("number of solutions that remained =", len(self.solution_to_solutions))
        for solution in added_solutions:
            self._add_solution(solution=solution)

        # Switch play.
        self.player = 1 - self.player

    def undo_move(self):
        """Undoes the most recent move.

        Raises:
            (AssertionError): if the internal state of the GraphManager is at the state given upon initialization.
        """
        added_problems = self.problem_manager.undo_move()
        for problem in added_problems:
            self._add_problem(problem=problem)

        added_solutions, removed_solutions = self.solution_manager.undo_move()
        for solution in removed_solutions:
            self._remove_solution(solution=solution)
        for solution in added_solutions:
            self._add_solution(solution=solution)
        for solution in self.solutions_removed_by_move.pop():
            self._add_solution(solution=solution)

        # Switch play.
        self.player = 1 - self.player

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
        problems = self.problem_manager.get_current_problems()

        if self.player == 0:
            return self._find_chosen_set(
                problems=problems,
                disallowed_solutions=self.white_solutions,
                used_solutions=set(),
            )

        if self.player == 1:
            # In order to prove White can win, White must be able to use a win condition and solve all problems
            # the win condition doesn't solve.
            for win_condition in self.solution_manager.get_win_conditions():
                chosen_set = self._find_chosen_set(
                    problems=problems - self.solution_to_problems[win_condition],
                    disallowed_solutions=self.black_solutions.union(self.solution_to_solutions[win_condition]),
                    used_solutions={win_condition},
                )
                if chosen_set is not None:
                    return chosen_set

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
        assert problems

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
