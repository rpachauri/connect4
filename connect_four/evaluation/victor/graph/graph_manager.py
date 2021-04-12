from typing import Set, Dict, List

from connect_four.problem import Group as Problem
from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.evaluation.victor.solution import combination
from connect_four.evaluation.victor.solution.solution2 import Solution
from connect_four.evaluation.victor.solution.solution_manager import SolutionManager
from connect_four.problem.problem_manager import ProblemManager


class GraphManager:
    def __init__(self, env_variables: TwoPlayerGameEnvVariables):
        """Initializes the SolutionManager with the given env_variables.

        Args:
            env_variables (TwoPlayerGameEnvVariables): a TwoPlayerGame's env_variables.
        """
        self.problem_manager = ProblemManager(env_variables=env_variables, num_to_connect=4)
        self.solution_manager = SolutionManager(env_variables=env_variables)

        solutions = self.solution_manager.get_solutions()

        self.problem_to_solutions, self.solution_to_problems, self.solution_to_solutions = self.create_node_graph(
            solutions=solutions,
            groups_by_square_by_player=self.problem_manager.groups_by_square_by_player,
        )

    @staticmethod
    def create_node_graph(
            solutions: Set[Solution], groups_by_square_by_player: List[List[List[Set[Problem]]]]
    ) -> (Dict[Problem, Set[Solution]], Dict[Solution, Set[Problem]], Dict[Solution, Set[Solution]]):
        """Creates a NodeGraph connecting Problems to Solutions, Solutions to Problems, and Solutions to Solutions.
        
        Args:
            solutions (Set[Solution]): the set of Solutions to include in the Graph.
            groups_by_square_by_player (List[List[List[Set[Group]]]]): a 3D array of a Set of Groups.
                1. The first dimension is the player.
                2. The second dimension is the row.
                3. The third dimension is the col.

                For a given player and a given (row, col),
                you can retrieve all Groups that player can win from that Square with:
                    set_of_possible_winning_groups_at_player_row_col = groups_by_square_by_player[player][row][col]

        Returns:
            problem_to_solutions (Dict[Problem, Set[Solution]]): dictionary mapping problems to solutions.
            solution_to_problems (Dict[Solution, Set[Problem]]): dictionary mapping solutions to problems.
            solution_to_solutions (Dict[Solution, Set[Solution]]): dictionary mapping solutions to solutions.
        """
        problem_to_solutions = {}
        solution_to_problems = {}
        solution_to_solutions = {}

        for solution in solutions:
            problems_solved = solution.rule_instance.find_problems_solved(
                groups_by_square_by_player=groups_by_square_by_player,
            )

            solution_to_problems[solution] = set()
            for problem in problems_solved:
                if problem not in problem_to_solutions:
                    problem_to_solutions[problem] = set()
                problem_to_solutions[problem].add(solution)
                solution_to_problems[solution].add(problem)

            solution_to_solutions[solution] = set()
            for other in solutions:
                if not combination.allowed(s1=solution, s2=other):
                    solution_to_solutions[solution].add(other)

        return problem_to_solutions, solution_to_problems, solution_to_solutions

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
        pass
