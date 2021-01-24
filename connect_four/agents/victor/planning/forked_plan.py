from collections import namedtuple

from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Lowinverse
from connect_four.agents.victor.rules import Highinverse
from connect_four.agents.victor.rules import Baseclaim

from connect_four.agents.victor.planning import simple_plan


Branch = namedtuple("Branch", ["forced_square", "simple_plan"])
Fork = namedtuple("Fork", ["branches"])


def from_lowinverse(lowinverse: Lowinverse) -> Fork:
    vertical0, vertical1 = tuple(lowinverse.verticals)
    return Fork(
        branches={
            vertical0.lower: Branch(
                forced_square=vertical0.upper,
                simple_plan=simple_plan.from_vertical(vertical1),
            ),
            vertical1.lower: Branch(
                forced_square=vertical1.upper,
                simple_plan=simple_plan.from_vertical(vertical0),
            ),
        }
    )


def from_highinverse(highinverse: Highinverse) -> Fork:
    lowinverse = highinverse.lowinverse
    vertical0, vertical1 = tuple(lowinverse.verticals)

    return Fork(
        branches={
            vertical0.lower: _create_highinverse_branch(
                vertical_a=vertical0,
                vertical_b=vertical1,
                directly_playable_squares=highinverse.directly_playable_squares,
            ),
            vertical1.lower: _create_highinverse_branch(
                vertical_a=vertical1,
                vertical_b=vertical0,
                directly_playable_squares=highinverse.directly_playable_squares,
            ),
        }
    )


def _create_highinverse_branch(vertical_a, vertical_b, directly_playable_squares) -> Branch:
    square_above_vertical_a = Square(row=vertical_a.upper.row - 1, col=vertical_a.upper.col)
    square_above_vertical_b = Square(row=vertical_b.upper.row - 1, col=vertical_b.upper.col)
    branch_simple_plan = simple_plan.from_claimeven(
        claimeven=Claimeven(
            upper=square_above_vertical_b,
            lower=vertical_b.upper,  # vertical_b.upper is the middle square of column b of the Highinverse.
        ),
    )
    if vertical_b.lower in directly_playable_squares:
        branch_simple_plan = branch_simple_plan.merge(
            simple_plan=simple_plan.from_baseinverse(
                baseinverse=Baseinverse(
                    playable1=vertical_b.lower,
                    playable2=square_above_vertical_a,
                ),
            ),
        )
    else:
        branch_simple_plan = branch_simple_plan.add_availabilities([vertical_b.lower, square_above_vertical_a])

    return Branch(
        forced_square=vertical_a.upper,
        simple_plan=branch_simple_plan,
    )


def from_baseclaim(baseclaim: Baseclaim) -> Fork:
    square_above_second = Square(row=baseclaim.second.row - 1, col=baseclaim.second.col)

    return Fork(
        branches={
            baseclaim.first: Branch(
                forced_square=baseclaim.third,
                simple_plan=simple_plan.from_claimeven(
                    claimeven=Claimeven(
                        lower=baseclaim.second,
                        upper=square_above_second,
                    ),
                )
            ),
            baseclaim.second: Branch(
                forced_square=baseclaim.third,
                simple_plan=simple_plan.from_baseinverse(
                    baseinverse=Baseinverse(
                        playable1=baseclaim.first,
                        playable2=square_above_second,
                    ),
                ),
            ),
            baseclaim.third: Branch(
                forced_square=baseclaim.second,
                simple_plan=simple_plan.from_baseinverse(
                    baseinverse=Baseinverse(
                        playable1=baseclaim.first,
                        playable2=square_above_second,
                    ),
                ),
            ),
        },
    )
