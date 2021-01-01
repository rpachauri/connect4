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
    return False


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
