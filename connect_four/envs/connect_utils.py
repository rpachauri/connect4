def connected(state, num_to_connect, player, row, col):
    """
    Args:
        state (np.ndarray): a numpy ndarray of shape (2, M, N), where M and N are > 0.
        num_to_connect (int): num_to_connect > 0.
        player (int): 0 or 1. The player we are checking.
        row (int): the starting row
        col (int): the starting column

    Requires:
        state[player, row, col] == 1

    Returns:
        connected_four (bool): True if the player connected at least num_to_connect using (row, col);
                           otherwise, False
    """
    row_and_col_adds = [
        (-1, 0),  # up
        (-1, 1),  # up-right
        (0, 1),  # right
        (1, 1),  # down-right
    ]
    for row_add, col_add in row_and_col_adds:
        num_tokens_in_pos_direction = _num_tokens_in_direction(state, player, row, col, row_add, col_add)
        num_tokens_in_neg_direction = _num_tokens_in_direction(state, player, row, col, -row_add, -col_add)
        num_tokens_in_line = num_tokens_in_pos_direction + 1 + num_tokens_in_neg_direction

        if num_tokens_in_line >= num_to_connect:
            return True

    # Player did not connect four in any direction.
    return False


def _num_tokens_in_direction(state, player, row, col, row_add, col_add):
    """ Finds the number of tokens belonging to the given player starting
    from the given location and continuing in the given direction.

    Args:
        player (int): 0 or 1. The player we are checking.
        row (int): the starting row
        col (int): the starting column
        row_add (int): the increment for row
        col_add (int): the increment for col

    Returns:
        The number of tokens belonging to the player in the given direction.
        The starting location is not included.
        E.g. If there is only 1 token belonging to the player
        adjacent to the given location, returns 1.
"""
    player_tokens = state[player]
    r, c = row, col
    num_tokens = -1

    # while we are still in bounds and the location belongs to the player.
    while (0 <= r < len(player_tokens) and 0 <= c < len(player_tokens[0]) and
           player_tokens[r, c] == 1):
        r += row_add
        c += col_add
        num_tokens += 1
    return num_tokens
