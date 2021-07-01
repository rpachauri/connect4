from connect_four.evaluation.victor.rules import Claimeven, Baseinverse, Vertical, Aftereven, Baseclaim, Before, \
    Specialbefore, Lowinverse, Highinverse, OddThreat

from connect_four.evaluation.victor.solution.victor_solution import VictorSolution


def allowed(s1: VictorSolution, s2: VictorSolution) -> bool:
    """Returns True if the two Solutions can be combined; Otherwise, False.

    Args:
        s1 (VictorSolution): a Solution.
        s2 (VictorSolution): a Solution.

    Returns:
        combination_allowed (bool): True if the two Solutions can be combined; Otherwise, False.
    """
    # If either VictorSolution is an OddThreat.
    if isinstance(s1.rule_instance, OddThreat):
        return allowed_with_odd_threat(solution=s1, other=s2)
    if isinstance(s2.rule_instance, OddThreat):
        return allowed_with_odd_threat(solution=s2, other=s1)

    # If either VictorSolution is a Claimeven.
    if isinstance(s1.rule_instance, Claimeven):
        return allowed_with_claimeven(solution=s1, other=s2)
    if isinstance(s2.rule_instance, Claimeven):
        return allowed_with_claimeven(solution=s2, other=s1)

    # If either VictorSolution is a Baseinverse:
    if isinstance(s1.rule_instance, Baseinverse):
        return allowed_with_baseinverse(solution=s1, other=s2)
    if isinstance(s2.rule_instance, Baseinverse):
        return allowed_with_baseinverse(solution=s2, other=s1)

    # If either VictorSolution is a Vertical:
    if isinstance(s1.rule_instance, Vertical):
        return allowed_with_vertical(solution=s1, other=s2)
    if isinstance(s2.rule_instance, Vertical):
        return allowed_with_vertical(solution=s2, other=s1)

    # If either VictorSolution is an Aftereven:
    if isinstance(s1.rule_instance, Aftereven):
        return allowed_with_aftereven(solution=s1, other=s2)
    if isinstance(s2.rule_instance, Aftereven):
        return allowed_with_aftereven(solution=s2, other=s1)

    # If either VictorSolution is a Lowinverse:
    if isinstance(s1.rule_instance, Lowinverse):
        return allowed_with_lowinverse(solution=s1, other=s2)
    if isinstance(s2.rule_instance, Lowinverse):
        return allowed_with_lowinverse(solution=s2, other=s1)

    # If either VictorSolution is a Highinverse:
    if isinstance(s1.rule_instance, Highinverse):
        return allowed_with_highinverse(solution=s1, other=s2)
    if isinstance(s2.rule_instance, Highinverse):
        return allowed_with_highinverse(solution=s2, other=s1)

    # If either VictorSolution is a Baseclaim:
    if isinstance(s1.rule_instance, Baseclaim):
        return allowed_with_baseclaim(solution=s1, other=s2)
    if isinstance(s2.rule_instance, Baseclaim):
        return allowed_with_baseclaim(solution=s2, other=s1)

    # If either VictorSolution is a Before:
    if isinstance(s1.rule_instance, Before):
        return allowed_with_before(solution=s1, other=s2)
    if isinstance(s2.rule_instance, Before):
        return allowed_with_before(solution=s2, other=s1)

    # If either VictorSolution is a Specialbefore: (although at this point, this must be true).
    if isinstance(s1.rule_instance, Specialbefore):
        return allowed_with_specialbefore(solution=s1, other=s2)
    if isinstance(s2.rule_instance, Specialbefore):
        return allowed_with_specialbefore(solution=s2, other=s1)

    raise ValueError("Unacceptable Rule types:", s1.rule_instance, s2.rule_instance)


def disjoint(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns True if the sets of squares are disjoint. Otherwise, False.

    Args:
        solution (VictorSolution): a Solution.
        other (VictorSolution): a Solution.

    Returns:
        True if the sets of squares are disjoint. Otherwise, False
    """
    return solution.squares.isdisjoint(other.squares)


def no_claimeven_below_or_at_inverse(inverse_solution: VictorSolution, claimeven_solution: VictorSolution) -> bool:
    """Returns True if there is no Claimeven in claimeven_solution below or at the Inverse of inverse_solution.

    Args:
        inverse_solution (VictorSolution): either a Lowinverse or Highinverse Solution.
        claimeven_solution (VictorSolution): a Claimeven, Aftereven, Baseclaim, Before, or Specialbefore Solution.

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


def column_wise_disjoint(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns true if the two solutions are disjoint (column-wise).

    Args:
        solution (VictorSolution): a Solution.
        other (VictorSolution): a Solution.

    Returns:
        False if the two solutions have squares that share a column,
        Otherwise, True.
    """
    return solution.squares_by_column.keys().isdisjoint(other.squares_by_column.keys())


def column_wise_disjoint_or_equal(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns true if the two solutions are disjoint or equal (column-wise).

    Args:
        solution (VictorSolution): a Solution.
        other (VictorSolution): a Solution.

    Returns:
        False if the two solutions have intersecting squares in a column,
        but the sets squares in that column are not equal.
        Otherwise, True.
    """
    for col in solution.squares_by_column:
        if col in other.squares_by_column:
            # If the two sets of Squares are not equal but share a Square:
            if (solution.squares_by_column[col].intersection(other.squares_by_column[col]) and
                    solution.squares_by_column[col] != other.squares_by_column[col]):
                return False
    return True


def allowed_with_odd_threat(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (VictorSolution): a Solution with rule=Rule.Claimeven.
        other (VictorSolution): a Solution.

    Requires:
        1. solution must have rule=Rule.Claimeven.
        2. other must have rule be one of the following:
            -   Rule.OddThreat
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
    # No OddThreat can be combined with another OddThreat.
    if isinstance(other.rule_instance, OddThreat):
        return False

    # OddThreats cannot be combined with any other VictorSolution that uses a square in the same column.
    if not column_wise_disjoint(solution=solution, other=other):
        return False

    # OddThreats are Solutions that belong to White. They cannot be combined with Black-only Solutions.
    if isinstance(other.rule_instance, (Aftereven, Before)):
        if other.rule_instance.group.player == 1:
            return False

    if isinstance(other.rule_instance, Specialbefore):
        if other.rule_instance.before.group.player == 1:
            return False

    return True


def allowed_with_claimeven(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (VictorSolution): a Solution with rule=Rule.Claimeven.
        other (VictorSolution): a Solution.

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
    if isinstance(other.rule_instance, (Claimeven, Baseinverse, Vertical, Aftereven, Baseclaim, Before, Specialbefore)):
        return disjoint(solution=solution, other=other)
    if isinstance(other.rule_instance, (Lowinverse, Highinverse)):
        return no_claimeven_below_or_at_inverse(inverse_solution=other, claimeven_solution=solution)
    raise ValueError("invalid other.rule_instance for allowed_with_claimeven:", other.rule_instance)


def allowed_with_baseinverse(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (VictorSolution): a Solution with rule=Rule.Baseinverse.
        other (VictorSolution): a Solution.

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


def allowed_with_vertical(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (VictorSolution): a Solution with rule=Rule.Vertical.
        other (VictorSolution): a Solution.

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


def allowed_with_aftereven(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (VictorSolution): a Solution with rule=Rule.Aftereven.
        other (VictorSolution): a Solution.

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
    if isinstance(other.rule_instance, (Aftereven, Before, Specialbefore)):
        return column_wise_disjoint_or_equal(solution=solution, other=other)
    if isinstance(other.rule_instance, (Lowinverse, Highinverse)):
        return (disjoint(solution=solution, other=other) and
                no_claimeven_below_or_at_inverse(inverse_solution=other, claimeven_solution=solution))
    if isinstance(other.rule_instance, Baseclaim):
        return disjoint(solution=solution, other=other)
    raise ValueError("invalid other.rule for allowed_with_aftereven:", other.rule_instance)


def allowed_with_lowinverse(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (VictorSolution): a Solution with rule=Rule.Lowinverse.
        other (VictorSolution): a Solution.

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
    if isinstance(other.rule_instance, (Lowinverse, Highinverse)):
        return disjoint(solution=solution, other=other)
    if isinstance(other.rule_instance, Baseclaim):
        return (disjoint(solution=solution, other=other) and
                no_claimeven_below_or_at_inverse(inverse_solution=solution, claimeven_solution=other))
    if isinstance(other.rule_instance, (Before, Specialbefore)):
        return (no_claimeven_below_or_at_inverse(inverse_solution=solution, claimeven_solution=other) and
                column_wise_disjoint_or_equal(solution=solution, other=other))


def allowed_with_highinverse(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (VictorSolution): a Solution with rule=Rule.Highinverse.
        other (VictorSolution): a Solution.

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
    if isinstance(other.rule_instance, Highinverse):
        return disjoint(solution=solution, other=other)
    if isinstance(other.rule_instance, (Baseclaim, Before, Specialbefore)):
        return (disjoint(solution=solution, other=other) and
                no_claimeven_below_or_at_inverse(inverse_solution=solution, claimeven_solution=other))
    raise ValueError("invalid other.rule for allowed_with_aftereven:", other.rule_instance)


def allowed_with_baseclaim(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (VictorSolution): a Solution with rule=Rule.Baseclaim.
        other (VictorSolution): a Solution.

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


def allowed_with_before(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (VictorSolution): a Solution with rule=Rule.Before.
        other (VictorSolution): a Solution.

    Requires:
        1. solution must have rule=Rule.Before.
        2. other must have rule be one of the following:
            -   Rule.Before
            -   Rule.Specialbefore

    Returns:
        combination_allowed (bool): True if other can be combined with solution; Otherwise, False.
    """
    return column_wise_disjoint_or_equal(solution=solution, other=other)


def allowed_with_specialbefore(solution: VictorSolution, other: VictorSolution) -> bool:
    """Returns True if other can be combined with solution; Otherwise, False.

    Args:
        solution (VictorSolution): a Solution with rule=Rule.Specialbefore.
        other (VictorSolution): a Solution.

    Requires:
        1. solution must have rule=Rule.Specialbefore.
        2. other must have rule be one of the following:
            -   Rule.Specialbefore

    Returns:
        combination_allowed (bool): True if other can be combined with solution; Otherwise, False.
    """
    if isinstance(solution.rule_instance, Specialbefore):  # Should be true.
        solution_baseinverse_squares = {
            solution.rule_instance.internal_directly_playable_square,
            solution.rule_instance.external_directly_playable_square,
        }
        if not solution_baseinverse_squares.isdisjoint(other.squares):
            return False
    return column_wise_disjoint_or_equal(solution=solution, other=other)
