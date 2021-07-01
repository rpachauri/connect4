from abc import abstractmethod
from typing import List, Set

from connect_four.problem import Group


class Rule:

    @abstractmethod
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
        pass

    @abstractmethod
    def solves(self, group: Group) -> bool:
        """Returns whether or not this Rule solves the given Group.

        Args:
            group (Group): Group being considered.

        Returns:
            solves (bool): True if this Rule instance solves the given Group; otherwise, false.
        """
        pass

    @abstractmethod
    def is_useful(self, groups: Set[Group]) -> bool:
        """Returns whether or not this Rule would be considered useful given that this is the set of Groups it solves.

        Requires:
            1. For every group in groups, self.solves(group) must be True.

        Args:
            groups (Set[Group]): a set of Groups that this Rule instance solves.

        Returns:
            is_useful (bool): True if this Rule instance is useful; otherwise, false.
        """
        pass
