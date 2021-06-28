from typing import Set

from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.rules import find_all_claimevens, find_all_baseinverses, find_all_verticals, \
    find_all_afterevens, find_all_lowinverses, find_all_highinverses, find_all_baseclaims, find_all_befores, \
    find_all_specialbefores, find_all_odd_threats, OddThreat
from connect_four.evaluation.victor.rules.aftereven import AfterevenManager
from connect_four.evaluation.victor.rules.baseclaim import BaseclaimManager
from connect_four.evaluation.victor.rules.baseinverse import BaseinverseManager
from connect_four.evaluation.victor.rules.before import BeforeManager
from connect_four.evaluation.victor.rules.claimeven import ClaimevenManager
from connect_four.evaluation.victor.rules.highinverse import HighinverseManager
from connect_four.evaluation.victor.rules.lowinverse import LowinverseManager
from connect_four.evaluation.victor.rules.specialbefore import SpecialbeforeManager
from connect_four.evaluation.victor.rules.vertical import VerticalManager
from connect_four.evaluation.victor.solution import solution2
from connect_four.evaluation.victor.solution.solution2 import Solution
from connect_four.evaluation.victor.solution.solution_manager import SolutionManager
from connect_four.game import Square


class VictorSolutionManager(SolutionManager):
    def __init__(self, env_variables: TwoPlayerGameEnvVariables):
        """Initializes the VictorSolutionManager with the given env_variables.

        Args:
            env_variables (TwoPlayerGameEnvVariables): a TwoPlayerGame's env_variables.
        """
        self.board = Board(env_variables=env_variables)
        # self.solutions_by_move = [self._find_all_solutions(board=self.board)]
        self.solutions = self._find_all_solutions(board=self.board)
        self.moves = []

    @staticmethod
    def _find_all_solutions(board: Board) -> Set[Solution]:
        """Finds all Solutions for the current board.

        Returns:
            solutions (Set[Solution]): the set of all Solutions for either player in the current board.
        """
        white_groups = board.potential_groups(0)
        black_groups = board.potential_groups(1)

        # Find all applications of all rules.
        claimevens = find_all_claimevens(board=board)
        baseinverses = find_all_baseinverses(board=board)
        verticals = find_all_verticals(board=board)
        white_afterevens = find_all_afterevens(board=board, opponent_groups=white_groups)
        black_afterevens = find_all_afterevens(board=board, opponent_groups=black_groups)
        lowinverses = find_all_lowinverses(verticals=verticals)
        highinverses = find_all_highinverses(board=board, lowinverses=lowinverses)
        baseclaims = find_all_baseclaims(board=board)
        white_befores = find_all_befores(board=board, opponent_groups=white_groups)
        white_specialbefores = find_all_specialbefores(board=board, befores=white_befores)
        black_befores = find_all_befores(board=board, opponent_groups=black_groups)
        black_specialbefores = find_all_specialbefores(board=board, befores=black_befores)
        # Find all win conditions for White.
        white_odd_threats = find_all_odd_threats(board=board)

        # Convert the rule instances into Solutions.
        solutions = set()
        for claimeven in claimevens:
            solutions.add(solution2.from_claimeven(claimeven=claimeven))
        for baseinverse in baseinverses:
            solutions.add(solution2.from_baseinverse(baseinverse=baseinverse))
        for vertical in verticals:
            solutions.add(solution2.from_vertical(vertical=vertical))
        for aftereven in white_afterevens:
            solutions.add(solution2.from_aftereven(aftereven=aftereven))
        for aftereven in black_afterevens:
            solutions.add(solution2.from_aftereven(aftereven=aftereven))
        for lowinverse in lowinverses:
            solutions.add(solution2.from_lowinverse(lowinverse=lowinverse))
        for highinverse in highinverses:
            solutions.add(solution2.from_highinverse(highinverse=highinverse))
        for baseclaim in baseclaims:
            solutions.add(solution2.from_baseclaim(baseclaim=baseclaim))
        for before in white_befores:
            solutions.add(solution2.from_before(before=before))
        for before in black_befores:
            solutions.add(solution2.from_before(before=before))
        for specialbefore in white_specialbefores:
            solutions.add(solution2.from_specialbefore(specialbefore=specialbefore))
        for specialbefore in black_specialbefores:
            solutions.add(solution2.from_specialbefore(specialbefore=specialbefore))
        # for odd_threat in white_odd_threats:
        #     solutions.add(solution2.from_odd_threat(odd_threat=odd_threat))

        return solutions

    def move(self, player: int, row: int, col: int) -> (Set[Solution], Set[Solution]):
        """Plays a move at the given row and column for the given player.

        Assumptions:
            1.  The internal state of the VictorSolutionManager is not at a terminal state.

        Args:
            player (int): the player making the move.
            row (int): the row to play
            col (int): the column to play

        Returns:
            removed_solutions (Set[Solution]): the Solutions that were removed after the given move.
            added_solutions (Set[Solution]): the Solutions that were added after the given move.
        """
        removed_solutions, added_solutions = VictorSolutionManager.added_removed_solutions(
            player=player, row=row, col=col, board=self.board,
        )
        self.solutions.difference_update(removed_solutions)
        self.solutions.update(added_solutions)

        self.board.state[player][row][col] = 1
        self.moves.append((player, row, col))

        return removed_solutions, added_solutions

    @staticmethod
    def added_removed_solutions(player: int, row: int, col: int, board: Board) -> (Set[Solution], Set[Solution]):
        claimeven_manager = ClaimevenManager(board=board)
        baseinverse_manager = BaseinverseManager(board=board)
        vertical_manager = VerticalManager(board=board)
        aftereven_manager = AfterevenManager(board=board)
        lowinverse_manager = LowinverseManager(verticals=vertical_manager.verticals)
        highinverse_manager = HighinverseManager(board=board, lowinverses=lowinverse_manager.lowinverses)
        baseclaim_manager = BaseclaimManager(board=board)
        before_manager = BeforeManager(board=board)
        specialbefore_manager = SpecialbeforeManager(board=board, befores=before_manager.befores)

        square = Square(row=row, col=col)
        playable_squares = board.playable_squares()

        claimeven = claimeven_manager.move(row=row, col=col)
        removed_baseinverses, added_baseinverses = baseinverse_manager.move(
            square=square,
            playable_squares=playable_squares,
        )
        vertical = vertical_manager.move(square=square)
        removed_afterevens, added_afterevens = aftereven_manager.move(player=player, square=square, board=board)
        removed_lowinverses = lowinverse_manager.move(
            vertical=vertical,
            verticals=vertical_manager.verticals,
        )
        removed_highinverses, added_highinverses = highinverse_manager.move(
            square=square,
            removed_lowinverses=removed_lowinverses,
            verticals=vertical_manager.verticals,
            directly_playable_squares=playable_squares,
        )
        removed_baseclaims, added_baseclaims = baseclaim_manager.move(
            square=square,
            directly_playable_squares=playable_squares,
        )
        removed_befores, added_befores = before_manager.move(player=player, square=square, board=board)
        removed_specialbefores, added_specialbefores = specialbefore_manager.move(
            square=square,
            board=board,
            removed_befores=removed_befores,
            added_befores=added_befores,
            befores=before_manager.befores - removed_befores - added_befores,
        )

        # Convert the rule instances into Solutions.
        removed_solutions = set()
        if claimeven is not None:
            removed_solutions.add(solution2.from_claimeven(claimeven=claimeven))
        for baseinverse in removed_baseinverses:
            removed_solutions.add(solution2.from_baseinverse(baseinverse=baseinverse))
        if vertical is not None:
            removed_solutions.add(solution2.from_vertical(vertical=vertical))
        for aftereven in removed_afterevens:
            removed_solutions.add(solution2.from_aftereven(aftereven=aftereven))
        for lowinverse in removed_lowinverses:
            removed_solutions.add(solution2.from_lowinverse(lowinverse=lowinverse))
        for highinverse in removed_highinverses:
            removed_solutions.add(solution2.from_highinverse(highinverse=highinverse))
        for baseclaim in removed_baseclaims:
            removed_solutions.add(solution2.from_baseclaim(baseclaim=baseclaim))
        for before in removed_befores:
            removed_solutions.add(solution2.from_before(before=before))
        for specialbefore in removed_specialbefores:
            removed_solutions.add(solution2.from_specialbefore(specialbefore=specialbefore))

        added_solutions = set()
        for baseinverse in added_baseinverses:
            added_solutions.add(solution2.from_baseinverse(baseinverse=baseinverse))
        for aftereven in added_afterevens:
            added_solutions.add(solution2.from_aftereven(aftereven=aftereven))
        for highinverse in added_highinverses:
            added_solutions.add(solution2.from_highinverse(highinverse=highinverse))
        for baseclaim in added_baseclaims:
            added_solutions.add(solution2.from_baseclaim(baseclaim=baseclaim))
        for before in added_befores:
            added_solutions.add(solution2.from_before(before=before))
        for specialbefore in added_specialbefores:
            added_solutions.add(solution2.from_specialbefore(specialbefore=specialbefore))

        return removed_solutions, added_solutions

    def undo_move(self) -> (Set[Solution], Set[Solution]):
        """Undoes the most recent move.

        Raises:
            (AssertionError): if the internal state of the VictorSolutionManager
                is at the state given upon initialization.

        Returns:
            added_solutions (Set[Solution]): the Solutions that were added by undoing the most recent move.
            removed_solutions (Set[Solution]): the Solutions that were removed by undoing the most recent move.
        """
        assert self.moves
        # current_solutions = self._find_all_solutions(board=self.board)

        player, row, col = self.moves.pop()
        self.board.state[player][row][col] = 0

        added_solutions, removed_solutions = VictorSolutionManager.added_removed_solutions(
            player=player, row=row, col=col, board=self.board,
        )
        self.solutions.update(added_solutions)
        self.solutions.difference_update(removed_solutions)

        return added_solutions, removed_solutions

    def get_solutions(self) -> Set[Solution]:
        """Returns all Solutions for the current game position.

        Returns:
            solutions (Set[Solution]): the set of all Solutions that can be used in the current state.
        """
        # return self.solutions_by_move[-1]
        return self._find_all_solutions(board=self.board)

    def get_win_conditions(self) -> Set[Solution]:
        """Returns all win conditions for the current game position.

        Returns:
            win_conditions (Set[Solution]): a subset of all Solutions in this state.

            Constraints on win_conditions:
                1. No Solution in win_conditions may be combined with another Solution in win_conditions.
        """
        win_conditions = set()

        # for solution in self.solutions_by_move[-1]:
        for solution in self._find_all_solutions(board=self.board):
            if isinstance(solution.rule_instance, OddThreat):
                win_conditions.add(solution)

        return win_conditions
