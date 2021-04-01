from connect_four.hashing.data_structures import Square, Group, SquareType
from typing import Dict, Set, List


def play_squares_from_state(state,
                            groups_by_square_by_player: List[List[List[Set[Group]]]],
                            square_types: List[List[SquareType]]):
    for player in range(len(state)):
        for row in range(len(state[0])):
            for col in range(len(state[0][0])):
                if state[player][row][col] == 1:
                    play_square(
                        player=player,
                        row=row,
                        col=col,
                        groups_by_square_by_player=groups_by_square_by_player,
                        square_types=square_types,
                    )


def play_square(player: int, row: int, col: int,
                groups_by_square_by_player: List[List[List[Set[Group]]]],
                square_types: List[List[SquareType]]) -> (Dict[Square, Set[Group]], Dict[Square, SquareType]):
    """

    Args:
        player (int): the player making the move.
        row (int): the row to make the move in.
        col (int): the column to make the move in.
        groups_by_square_by_player (List[List[List[Set[Group]]]]): The possible Groups a player can win at a square.
        square_types (List[List[SquareType]]): The SquareType for each square.

    Returns:
        groups_removed_by_squares (Dict[Square, Set[Group]]):
            A Dictionary mapping Squares to all Groups that were removed.
            For every square in groups_removed_by_squares, the opponent can no longer win using that Group.
        previous_square_types (Dict[Square, SquareType]):
            A Dictionary mapping Squares to the SquareType they were before this move was played.
            Only Squares that had their SquareType changed are included.
    """
    # Change groups_by_square_by_player to reflect that the opponent cannot win using any group in groups.
    # Also, retrieve groups_removed_by_square.
    groups_removed_by_square = remove_groups(
        row=row,
        col=col,
        existing_groups_by_square=groups_by_square_by_player[1 - player],
    )

    # Find all indifferent squares.
    indifferent_squares = find_indifferent_squares(
        player=player,
        row=row,
        col=col,
        groups_removed_by_square=groups_removed_by_square,
        square_types=square_types,
        existing_groups_by_square_by_player=groups_by_square_by_player,
    )

    # Change the square types of indifferent squares.
    # Also, find the SquareType of all squares that are being changed.
    previous_square_types = update_square_types(
        row=row,
        col=col,
        indifferent_squares=indifferent_squares,
        square_types=square_types,
    )

    return groups_removed_by_square, previous_square_types


def remove_groups(row: int, col: int,
                  existing_groups_by_square: List[List[Set[Group]]]) -> Dict[Square, Set[Group]]:
    """
    Args:
        row (int):
        col (int):
        existing_groups_by_square (List[List[Set[Group]]]): a 2D array containing a set of Groups at each cell.
            This set of Groups are all existing Groups the opponent can use to win at that square.

    Modifies:
        existing_groups_by_square: For every square in groups_removed_by_squares,
            every group in groups_removed_by_squares[square] will be removed from existing_groups_by_square.

    Returns:
        groups_removed_by_square (Dict[Square, Set[Group]]):
            A Dictionary mapping Squares to all Groups that were removed.
            For every square in groups_removed_by_squares, the opponent can no longer win using that Group.
    """
    groups_to_remove = existing_groups_by_square[row][col].copy()
    # Change existing_groups_by_square to reflect that the opponent cannot win using any group in groups.
    groups_removed_by_square = {}
    for g in groups_to_remove:
        for s in g.squares:
            # If the opponent could win using this group, they no longer can.
            if g in existing_groups_by_square[s.row][s.col]:
                existing_groups_by_square[s.row][s.col].remove(g)

                # If groups_removed_by_square doesn't already contain this square, add it.
                if s not in groups_removed_by_square:
                    groups_removed_by_square[s] = set()

                # Add g as one of the groups removed.
                groups_removed_by_square[s].add(g)
    return groups_removed_by_square


def find_indifferent_squares(player: int, row: int, col: int,
                             groups_removed_by_square: Dict[Square, Set[Group]],
                             square_types: List[List[SquareType]],
                             existing_groups_by_square_by_player: List[List[List[Set[Group]]]]) -> Set[Square]:
    """

    Args:
        player (int):
        row (int):
        col (int):
        groups_removed_by_square (Dict[Square, Set[Group]]):
            A Dictionary mapping Squares to all Groups that were removed.
            For every square in groups_removed_by_squares, the opponent can no longer win using that Group.
        square_types (List[List[SquareType]]): a 2D array of the current SquareTypes.
        existing_groups_by_square_by_player (List[List[List[Set[Group]]]]):
            A 3D array containing a set of Groups at each cell.
            First dimension is the player. Second dimension is the row. Third dimension is the column.
            The Set of Groups at the cell are all existing Groups the player can use to win at that square.

    Modifies:
        square_types: If the square at the given row and col is not indifferent,
            assigns a SquareType corresponding with the given player.
            Updates all squares that are indifferent to SquareType.Indifferent.

    Returns:
        indifferent_squares (Set[Square]): a Set of Squares that can no longer be used to
            complete any Groups for either player.
    """
    # Assign the played square a non-empty SquareType. This allows it be included when finding indifferent_squares.
    if player == 0:
        square_types[row][col] = SquareType.Player1
    else:
        square_types[row][col] = SquareType.Player2

    # Find all indifferent squares.
    indifferent_squares = set()
    if not groups_removed_by_square:
        indifferent_squares.add(Square(row=row, col=col))
    for s in groups_removed_by_square:
        # If neither player can win any groups at this square, this square is indifferent.
        if (square_types[s.row][s.col] != SquareType.Empty) and \
                (not existing_groups_by_square_by_player[0][s.row][s.col]) and \
                (not existing_groups_by_square_by_player[1][s.row][s.col]):
            indifferent_squares.add(s)
    return indifferent_squares


def update_square_types(row: int, col: int,
                        indifferent_squares: Set[Square],
                        square_types: List[List[SquareType]]) -> Dict[Square, SquareType]:
    """

    Args:
        row (int):
        col (int):
        indifferent_squares (Set[Square]): a Set of Squares that can no longer be used to
            complete any Groups for either player.
        square_types (List[List[SquareType]]): a 2D array of the current SquareTypes.

    Modifies:
        square_types: For every square in indifferent_squares, updates to SquareType.Indifferent.

    Returns:
        previous_square_types (Dict[Square, SquareType]): a dictionary mapping each Square to the SquareType it was
            before it was changed.
    """
    # Find the SquareType of all squares that are being changed.
    previous_square_types = {}
    # Change the square types of indifferent squares.
    for s in indifferent_squares:
        previous_square_types[s] = square_types[s.row][s.col]
        square_types[s.row][s.col] = SquareType.Indifferent

    previous_square_types[Square(row=row, col=col)] = SquareType.Empty

    return previous_square_types
