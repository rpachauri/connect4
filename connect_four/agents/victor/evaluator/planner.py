# TODO deprecate.
from connect_four.agents.victor.planning.plan import Plan


def convert(solutions) -> Plan:
    """convert converts a set of Solutions into a Plan.

    Args:
        solutions (Set<Solution>): a set of Solutions.

    Returns:
        plan (Plan): a Plan.
    """
    plan = Plan()
    for solution in solutions:
        plan.responses.update(solution.plan.responses)
        plan.availabilities.update(solution.plan.availabilities)

    return plan
