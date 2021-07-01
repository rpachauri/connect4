from typing import List, Set, Optional

from connect_four.evaluation.victor.rules import Rule, Claimeven
from connect_four.game import Square
from connect_four.problem import Group, GroupDirection
from connect_four.evaluation.victor.board import Board

import warnings


class Aftereven(Rule):
    def __init__(self, group: Group, claimevens):
        """Initializes an Aftereven instance.

        Args:
            group (Group): a group representing the Aftereven group.
            claimevens (iterable<Claimeven>): an iterable of Claimevens which are part of the Aftereven.
        """
        self.group = group
        self.claimevens = frozenset(claimevens)

    def __eq__(self, other):
        if isinstance(other, Aftereven):
            return self.group == other.group and self.claimevens == other.claimevens
        return False

    def __hash__(self):
        return self.group.__hash__() * 31 + self.claimevens.__hash__()

    def empty_squares_of_aftereven_group(self):
        empty_squares = []

        for claimeven in self.claimevens:
            # claimeven.upper should be an empty square part of the Aftereven group by definition.
            # Otherwise, something is wrong.
            empty_squares.append(claimeven.upper)

        return empty_squares

    def solves(self, group: Group) -> bool:
        if group.player == self.group.player:
            return False

        for claimeven in self.claimevens:
            if claimeven.solves(group=group):
                return True

        return self.is_group_solvable_by_aftereven(group=group)

    def is_useful(self, groups: Set[Group]) -> bool:
        # Assuming every group in groups can be solved by this Aftereven, if there is a single Group that
        # cannot be solved by one of the Aftereven's Claimevens, then this Aftereven is useful.
        solved_claimeven_groups = set()
        for group in groups:
            for claimeven in self.claimevens:
                if claimeven.solves(group=group):
                    solved_claimeven_groups.add(group)

        # Given that solved_claimeven_groups is a subset of groups, it will not equal groups only if there exists
        # a Group this Aftereven can solve that one of its Claimevens cannot.
        return solved_claimeven_groups != groups

    def is_group_solvable_by_aftereven(self, group: Group) -> bool:
        """Returns whether or not group has at least one square in all Aftereven columns,
        above the empty square of the Aftereven group in that column

        Args:
            group (Group): a Group to be solved.

        Returns:
            is_group_solvable_by_aftereven (bool): true if this Aftereven solves group; otherwise, false.
        """
        empty_squares_of_aftereven = self.empty_squares_of_aftereven_group()

        # The Group must have one square above every empty square of the Aftereven Group.
        # If this is not the case, return False.
        for empty_square in empty_squares_of_aftereven:
            if not Aftereven.group_above_square(square=empty_square, group=group):
                return False

        # If all empty squares of the Aftereven Group is below a Square in group, return True.
        return True

    @staticmethod
    def group_above_square(square: Square, group: Group) -> bool:
        """Returns whether or not group contains a Square above square.

        Args:
            square (Square): a Square.
            group (Group): a Group.

        Returns:
            group_above_square (bool): True if group contains a Square above square; otherwise, false.
        """
        for square_in_group in group.squares:
            if square.col == square_in_group.col and square.row > square_in_group.row:
                return True
        return False

    def find_problems_solved(self, groups_by_square_by_player: List[List[List[Set[Group]]]]) -> Set[Group]:
        """Finds all Problems this Rule solves.

        Args:
            groups_by_square_by_player (List[List[List[Set[Group]]]]): a 3D array of a Set of Groups.
                1. The first dimension is the player.
                2. The second dimension is the row.
                3. The third dimension is the col.

                For a given player and a given (row, col),
                you can retrieve all Groups that player can win from that Square with:
                    set_of_possible_winning_groups_at_player_row_col = groups_by_square_by_player[player][row][col]

        Returns:
            problems_solved (Set[Group]): All Problems in square_to_groups this Rule solves.
        """
        warnings.warn("find_problems_solved is deprecated. use solves() instead", DeprecationWarning)
        groups = set()
        self.add_new_groups_from_aftereven(
            groups=groups,
            empty_squares_of_aftereven=self.empty_squares_of_aftereven_group(),
            threatening_squares=[],
            groups_by_square=groups_by_square_by_player[1 - self.group.player],
        )
        for claimeven in self.claimevens:
            groups.update(claimeven.find_problems_solved_for_player(
                groups_by_square=groups_by_square_by_player[1 - self.group.player],
            ))
        return groups

    @staticmethod
    def add_new_groups_from_aftereven(
            groups: Set[Group],
            empty_squares_of_aftereven: List[Square],
            threatening_squares: List[Square],
            groups_by_square: List[List[Set[Group]]]):
        """Adds any new groups that intersect squares above empty_squares_of_aftereven to groups.
        This is a recursive backtracking algorithm.
        threatening_squares starts out as an empty list.
        empty_squares_of_aftereven starts out as a list of all empty squares of the aftereven.

        We select a square from empty_squares_of_aftereven and remove it from the list.
        For every square above that square, we add it to threatening_squares, recurse, and then remove it from
          threatening_squares.
        The base case is when empty_squares_of_aftereven is empty. At that point, we find all groups that include
          all squares in threatening_squares and add them to groups.

        Args:
            groups (Set[Group]): a Set of groups this function will add to.
            empty_squares_of_aftereven (List[Square]):
                A subset of empty Squares that belong to an Aftereven.
                If two Squares from the Aftereven belong in the same column,
                    the Square from the higher row should be given.
                It is required that none of the Squares share the same column.
            threatening_squares (List[Square]):
                A list of Squares that could belong to a group that the Aftereven refutes.
                It is required that none of the Squares share the same column.
            groups_by_square (List[List[Set[Group]]]): A 2D array mapping each
                Square to all groups that contain that Square.

        Returns:
            None
        """
        # Base case.
        if not empty_squares_of_aftereven:
            new_groups_to_add = groups_by_square[threatening_squares[0].row][threatening_squares[0].col]
            for square in threatening_squares[1:]:
                new_groups_to_add = new_groups_to_add.intersection(groups_by_square[square.row][square.col])
            groups.update(new_groups_to_add)
            return

        # Recursive Case.
        square = empty_squares_of_aftereven.pop()
        for row in range(square.row - 1, -1, -1):
            square_above = Square(row=row, col=square.col)
            # Choose.
            threatening_squares.append(square_above)
            # Recurse.
            Aftereven.add_new_groups_from_aftereven(
                groups, empty_squares_of_aftereven, threatening_squares, groups_by_square)
            # Unchoose.
            threatening_squares.remove(square_above)
        empty_squares_of_aftereven.append(square)


def find_all_afterevens(board: Board, opponent_groups: Set[Group]) -> Set[Aftereven]:
    """find_all_afterevens takes a Board and a set of Claimevens and returns a set of Afterevens for the Board.

    Args:
        board (Board): a Board instance.
        opponent_groups (iterable<Group>): an iterable of Groups belonging to the
            opponent of the player to move on board.

    Returns:
        afterevens (set<Aftereven>): a set of Afterevens for board.
    """
    afterevens = set()
    for group in opponent_groups:
        aftereven_claimevens = AfterevenManager.get_aftereven_claimevens_excluding_square(board=board, group=group)
        # get_aftereven_claimevens(board, group)
        if aftereven_claimevens is not None:
            afterevens.add(Aftereven(group, aftereven_claimevens))

    return afterevens


class AfterevenManager:
    def __init__(self, board: Board):
        """Initializes the AfterevenManager.

        Args:
            board (Board): a Board instance.
        """
        self.afterevens = find_all_afterevens(board=board, opponent_groups=board.potential_groups(player=0))
        self.afterevens.update(find_all_afterevens(board=board, opponent_groups=board.potential_groups(player=1)))

    def move(self, player: int, square: Square, board: Board) -> (Set[Aftereven], Set[Aftereven]):
        """Moves the internal state of the AfterevenManager to after this square has been played.

        Args:
            player (int): the player playing square.
            square (Square): the square being played.
            board (Board): the Board state, without square having been played yet.

        Returns:
            removed_afterevens (Set[Aftereven]): the set of Afterevens being removed.
            added_afterevens (Set[Aftereven]): the set of Afterevens being added.
        """
        removed_afterevens = AfterevenManager.afterevens_above_square(square=square, board=board)
        self.afterevens.difference_update(removed_afterevens)

        added_afterevens = AfterevenManager.afterevens_at_square(player=player, square=square, board=board)
        self.afterevens.update(added_afterevens)

        return removed_afterevens, added_afterevens

    @staticmethod
    def afterevens_above_square(square: Square, board: Board) -> Set[Aftereven]:
        """Finds all Afterevens that uses the Square above square.

        Args:
            square (Square): the square being played.
                1. If square is even, returns an empty set.
                2. If square is odd, returns all Afterevens that contain the Claimeven that uses square as its lower.
            board (Board): the Board state, without square having been played yet.

        Returns:
            afterevens (Set[Aftereven]): a set of Afterevens.
                Each Aftereven in afterevens contains a Claimeven with square as its lower.
        """
        # If square is even, no Claimevens would be affected and thus, no Afterevens would be affected.
        if square.row % 2 == 0:
            return set()
        # square must be odd (i.e. the lower of a Claimeven).

        # Find all Groups that contain square_above.
        square_above = Square(row=square.row - 1, col=square.col)
        groups = board.potential_groups_at_square(square=square_above)

        afterevens = set()
        # Any Aftereven that uses a group in groups can no longer be used.
        for group in groups:
            aftereven_claimevens = AfterevenManager.get_aftereven_claimevens_excluding_square(board=board, group=group)
            if aftereven_claimevens is not None:
                afterevens.add(Aftereven(group, aftereven_claimevens))

        return afterevens

    @staticmethod
    def afterevens_at_square(player: int, square: Square, board: Board) -> Set[Aftereven]:
        """Finds all Afterevens that uses square.

        Args:
            player (int): the player playing square.
            square (Square): the square being played.
            board (Board): the Board state, without square having been played yet.

        Returns:
            afterevens (Set[Aftereven]): a set of Afterevens.
                Each Aftereven group in afterevens contains square.
        """
        # Find all Groups that contain square.
        groups = board.potential_groups_at_square(square=square)

        afterevens = set()
        # Any Aftereven that uses a group in groups can no longer be used.
        for group in groups:
            if group.player == player:
                aftereven_claimevens = AfterevenManager.get_aftereven_claimevens_excluding_square(
                    board=board,
                    group=group,
                    excluding_square=square,
                )
                if aftereven_claimevens is not None:
                    afterevens.add(Aftereven(group, aftereven_claimevens))

        return afterevens

    @staticmethod
    def get_aftereven_claimevens_excluding_square(board: Board, group: Group, excluding_square: Square = None) -> \
            Optional[Set[Claimeven]]:
        """get_aftereven_claimevens takes a Board, set of Claimevens, a Group, and a Square.
        It figures out if group could be an Aftereven group if Square was played by group.player.
        If the group is an Aftereven group, then it returns the Claimevens which are part of the Aftereven.
        If the group is not an Aftereven group, then it returns None.

        Args:
            board (Board): a Board instance.
            group (Group): a group on this board.
            excluding_square (Square): an empty Square part of group to exclude when searching for Claimevens.

        Returns:
            claimevens (iterable<Claimeven>):
                If the given group could be an Aftereven group, an iterable of Claimevens,
                where the upper square of each Claimeven is an empty square in the Aftereven group.

                If the given group is not an Aftereven group, returns None.
        """
        if group.direction == GroupDirection.vertical:
            return None

        claimevens = set()

        for square in group.squares:
            # If the square is not empty, we assume it already belongs to the player who owns the Group.
            if board.is_empty(square) and square != excluding_square:
                # If a square is in the top row, then this would be a useless Aftereven.
                if square.row == 0:
                    return None

                # If square is odd, then we cannot use a Claimeven to build the Aftereven.
                if square.row % 2 == 1:
                    return None

                lower = Square(row=square.row + 1, col=square.col)

                # If an even square of an Aftereven group is empty, but the square below it is not,
                # then it is not a Claimeven.
                if not board.is_empty(square=lower):
                    return None

                claimevens.add(Claimeven(lower=lower, upper=square))

        return claimevens

    def undo_move(self, player: int, square: Square, board: Board) -> (Set[Aftereven], Set[Aftereven]):
        """Undoes the most recent move, updating the set of Afterevens.

        Args:
            player (int): the player who had square.
            square (int): the square being undone.
            board (Board): the Board state, with square being empty.

        Returns:
            added_afterevens (Set[Aftereven]): the set of Afterevens being added.
            removed_afterevens (Set[Aftereven]): the set of Afterevens being removed.
        """
        added_afterevens = AfterevenManager.afterevens_above_square(square=square, board=board)
        self.afterevens.update(added_afterevens)

        removed_afterevens = AfterevenManager.afterevens_at_square(player=player, square=square, board=board)
        self.afterevens.difference_update(removed_afterevens)

        return added_afterevens, removed_afterevens
