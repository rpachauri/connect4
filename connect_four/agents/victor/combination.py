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
    return False


def disjoint(solution: Solution, other: Solution):
    """Returns True if the sets of squares are disjoint. Otherwise, False.

    Args:
        solution (Solution): a Solution.
        other (Solution): a Solution.

    Returns:
        True if the sets of squares are disjoint. Otherwise, False
    """
    return not solution.squares.intersection(other.squares)


def no_claimeven_below_or_at_inverse(inverse_solution: Solution, claimeven_solution: Solution):
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
    return True


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
    return False


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
    return False


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
    return False


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
    return False


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
    return False


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
    return False


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
    return False
