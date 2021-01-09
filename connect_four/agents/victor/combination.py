from connect_four.agents.victor import Rule

from connect_four.agents.victor import Solution


def allowed(s1: Solution, s2: Solution) -> bool:
    """Returns True if the two Solutions can be combined; Otherwise, False.

    Args:
        s1 (Solution): a Solution.
        s2 (Solution): a Solution.

    Returns:
        combination_allowed (bool): True if the two Solutions can be combined; Otherwise, False.
    """
    # If either Solution is a Claimeven.
    if s1.rule == Rule.Claimeven:
        return allowed_with_claimeven(solution=s1, other=s2)
    if s2.rule == Rule.Claimeven:
        return allowed_with_claimeven(solution=s2, other=s1)

    # If either Solution is a Baseinverse:
    if s1.rule == Rule.Baseinverse:
        return allowed_with_baseinverse(solution=s1, other=s2)
    if s2.rule == Rule.Baseinverse:
        return allowed_with_baseinverse(solution=s2, other=s1)

    # If either Solution is a Vertical:
    if s1.rule == Rule.Vertical:
        return allowed_with_vertical(solution=s1, other=s2)
    if s2.rule == Rule.Vertical:
        return allowed_with_vertical(solution=s2, other=s1)

    # If either Solution is an Aftereven:
    if s1.rule == Rule.Aftereven:
        return allowed_with_aftereven(solution=s1, other=s2)
    if s2.rule == Rule.Aftereven:
        return allowed_with_aftereven(solution=s2, other=s1)

    # If either Solution is a Lowinverse:
    if s1.rule == Rule.Lowinverse:
        return allowed_with_lowinverse(solution=s1, other=s2)
    if s2.rule == Rule.Lowinverse:
        return allowed_with_lowinverse(solution=s2, other=s1)

    # If either Solution is a Highinverse:
    if s1.rule == Rule.Highinverse:
        return allowed_with_highinverse(solution=s1, other=s2)
    if s2.rule == Rule.Highinverse:
        return allowed_with_highinverse(solution=s2, other=s1)

    # If either Solution is a Baseclaim:
    if s1.rule == Rule.Baseclaim:
        return allowed_with_baseclaim(solution=s1, other=s2)
    if s2.rule == Rule.Baseclaim:
        return allowed_with_baseclaim(solution=s2, other=s1)

    # If either Solution is a Before:
    if s1.rule == Rule.Before:
        return allowed_with_before(solution=s1, other=s2)
    if s2.rule == Rule.Before:
        return allowed_with_before(solution=s2, other=s1)

    # If either Solution is a Specialbefore: (although at this point, this must be true).
    if s1.rule == Rule.Specialbefore:
        return allowed_with_specialbefore(solution=s1, other=s2)
    if s2.rule == Rule.Specialbefore:
        return allowed_with_specialbefore(solution=s2, other=s1)

    raise ValueError("Unacceptable Rule types:", s1.rule, s2.rule)


def disjoint(solution: Solution, other: Solution) -> bool:
    """Returns True if the sets of squares are disjoint. Otherwise, False.

    Args:
        solution (Solution): a Solution.
        other (Solution): a Solution.

    Returns:
        True if the sets of squares are disjoint. Otherwise, False
    """
    return solution.squares.isdisjoint(other.squares)


def no_claimeven_below_or_at_inverse(inverse_solution: Solution, claimeven_solution: Solution) -> bool:
    """Returns True if there is no Claimeven in claimeven_solution below or at the Inverse of inverse_solution.

    Args:
        inverse_solution (Solution): either a Lowinverse or Highinverse Solution.
        claimeven_solution (Solution): a Claimeven, Aftereven, Baseclaim, Before, or Specialbefore Solution.

    Returns:
        False if there exists a lower Claimeven square in claimeven_solution equal to or
            above a square in inverse_solution.
        Otherwise, True.
    """
    #
    for i_square in inverse_solution.squares:
        for c_square in claimeven_solution.claimeven_bottom_squares:
            # If the inverse has a square above or equal to the bottom square of a Claimeven in other:
            if i_square.col == c_square.col and i_square.row <= c_square.row:
                return False
    return True


def column_wise_disjoint_or_equal(solution: Solution, other: Solution) -> bool:
    """Returns true if the two solutions are disjoint or equal (column-wise).

    Args:
        solution (Solution): a Solution.
        other (Solution): a Solution.

    Returns:
        False if the two solutions have intersecting squares in a column,
        but the sets squares in that column are not equal.
        Otherwise, True.
    """
    solution_cols_to_squares = cols_to_squares(solution.squares)
    other_cols_to_squares = cols_to_squares(other.squares)

    for col in solution_cols_to_squares:
        if col in other_cols_to_squares:
            # If the two sets of Squares are not equal but share a Square:
            if (solution_cols_to_squares[col].intersection(other_cols_to_squares[col]) and
                    solution_cols_to_squares[col] != other_cols_to_squares[col]):
                return False
    return True


def cols_to_squares(squares):
    """Converts an iterable of Squares into a dictionary of Squares keyed by the column they belong in.

    Args:
        squares (iterable<Square>): an iterable of Square objects.

    Returns:
        col_to_squares_dict (Map<int, Set<Square>>): a dictionary of columns to Squares in that column.
    """
    col_to_squares_dict = {}
    for square in squares:
        if square.col not in col_to_squares_dict:
            col_to_squares_dict[square.col] = set()
        col_to_squares_dict[square.col].add(square)
    return col_to_squares_dict


def allowed_with_claimeven(solution: Solution, other: Solution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (Solution): a Solution with rule=Rule.Claimeven.
        other (Solution): a Solution.

    Requires:
        1. solution must have rule=Rule.Claimeven.
        2. other must have rule be one of the following:
            -   Rule.Claimeven
            -   Rule.Baseinverse
            -   Rule.Vertical
            -   Rule.Aftereven
            -   Rule.Lowinverse
            -   Rule.Highinverse
            -   Rule.Baseclaim
            -   Rule.Before
            -   Rule.Specialbefore

    Returns:
        combination_allowed (bool): True if other can be combined with solution; Otherwise, False.
    """
    if other.rule in [
        Rule.Claimeven,
        Rule.Baseinverse,
        Rule.Vertical,
        Rule.Aftereven,
        Rule.Baseclaim,
        Rule.Before,
        Rule.Specialbefore,
    ]:
        return disjoint(solution=solution, other=other)
    if other.rule in [Rule.Lowinverse, Rule.Highinverse]:
        return no_claimeven_below_or_at_inverse(inverse_solution=other, claimeven_solution=solution)
    raise ValueError("invalid other.rule for allowed_with_claimeven:", other.rule)


def allowed_with_baseinverse(solution: Solution, other: Solution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (Solution): a Solution with rule=Rule.Baseinverse.
        other (Solution): a Solution.

    Requires:
        1. solution must have rule=Rule.Baseinverse.
        2. other must have rule be one of the following:
            -   Rule.Baseinverse
            -   Rule.Vertical
            -   Rule.Aftereven
            -   Rule.Lowinverse
            -   Rule.Highinverse
            -   Rule.Baseclaim
            -   Rule.Before
            -   Rule.Specialbefore

    Returns:
        combination_allowed (bool): True if other can be combined with solution; Otherwise, False.
    """
    return disjoint(solution=solution, other=other)


def allowed_with_vertical(solution: Solution, other: Solution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (Solution): a Solution with rule=Rule.Vertical.
        other (Solution): a Solution.

    Requires:
        1. solution must have rule=Rule.Vertical.
        2. other must have rule be one of the following:
            -   Rule.Vertical
            -   Rule.Aftereven
            -   Rule.Lowinverse
            -   Rule.Highinverse
            -   Rule.Baseclaim
            -   Rule.Before
            -   Rule.Specialbefore

    Returns:
        combination_allowed (bool): True if other can be combined with solution; Otherwise, False.
    """
    return disjoint(solution=solution, other=other)


def allowed_with_aftereven(solution: Solution, other: Solution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (Solution): a Solution with rule=Rule.Aftereven.
        other (Solution): a Solution.

    Requires:
        1. solution must have rule=Rule.Aftereven.
        2. other must have rule be one of the following:
            -   Rule.Aftereven
            -   Rule.Lowinverse
            -   Rule.Highinverse
            -   Rule.Baseclaim
            -   Rule.Before
            -   Rule.Specialbefore

    Returns:
        combination_allowed (bool): True if other can be combined with solution; Otherwise, False.
    """
    if other.rule in [Rule.Aftereven, Rule.Before, Rule.Specialbefore]:
        return column_wise_disjoint_or_equal(solution=solution, other=other)
    if other.rule in [Rule.Lowinverse, Rule.Highinverse]:
        return (disjoint(solution=solution, other=other) and
                no_claimeven_below_or_at_inverse(inverse_solution=other, claimeven_solution=solution))
    if other.rule in [Rule.Baseclaim]:
        return disjoint(solution=solution, other=other)
    raise ValueError("invalid other.rule for allowed_with_aftereven:", other.rule)


def allowed_with_lowinverse(solution: Solution, other: Solution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (Solution): a Solution with rule=Rule.Lowinverse.
        other (Solution): a Solution.

    Requires:
        1. solution must have rule=Rule.Lowinverse.
        2. other must have rule be one of the following:
            -   Rule.Lowinverse
            -   Rule.Highinverse
            -   Rule.Baseclaim
            -   Rule.Before
            -   Rule.Specialbefore

    Returns:
        combination_allowed (bool): True if other can be combined with solution; Otherwise, False.
    """
    return False


def allowed_with_highinverse(solution: Solution, other: Solution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (Solution): a Solution with rule=Rule.Highinverse.
        other (Solution): a Solution.

    Requires:
        1. solution must have rule=Rule.Highinverse.
        2. other must have rule be one of the following:
            -   Rule.Highinverse
            -   Rule.Baseclaim
            -   Rule.Before
            -   Rule.Specialbefore

    Returns:
        combination_allowed (bool): True if other can be combined with solution; Otherwise, False.
    """
    if other.rule in [Rule.Highinverse]:
        return disjoint(solution=solution, other=other)
    if other.rule in [Rule.Baseclaim, Rule.Before, Rule.Specialbefore]:
        return (disjoint(solution=solution, other=other) and
                no_claimeven_below_or_at_inverse(inverse_solution=solution, claimeven_solution=other))
    raise ValueError("invalid other.rule for allowed_with_aftereven:", other.rule)


def allowed_with_baseclaim(solution: Solution, other: Solution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (Solution): a Solution with rule=Rule.Baseclaim.
        other (Solution): a Solution.

    Requires:
        1. solution must have rule=Rule.Baseclaim.
        2. other must have rule be one of the following:
            -   Rule.Baseclaim
            -   Rule.Before
            -   Rule.Specialbefore

    Returns:
        combination_allowed (bool): True if other can be combined with solution; Otherwise, False.
    """
    return disjoint(solution=solution, other=other)


def allowed_with_before(solution: Solution, other: Solution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (Solution): a Solution with rule=Rule.Before.
        other (Solution): a Solution.

    Requires:
        1. solution must have rule=Rule.Before.
        2. other must have rule be one of the following:
            -   Rule.Before
            -   Rule.Specialbefore

    Returns:
        combination_allowed (bool): True if other can be combined with solution; Otherwise, False.
    """
    return column_wise_disjoint_or_equal(solution=solution, other=other)


def allowed_with_specialbefore(solution: Solution, other: Solution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (Solution): a Solution with rule=Rule.Specialbefore.
        other (Solution): a Solution.

    Requires:
        1. solution must have rule=Rule.Specialbefore.
        2. other must have rule be one of the following:
            -   Rule.Specialbefore

    Returns:
        combination_allowed (bool): True if other can be combined with solution; Otherwise, False.
    """
    return column_wise_disjoint_or_equal(solution=solution, other=other)
