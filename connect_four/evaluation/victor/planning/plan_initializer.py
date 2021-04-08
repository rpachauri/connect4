import copy

from connect_four.evaluation.victor.game import Board
from connect_four.evaluation.victor.evaluator import evaluator
from connect_four.evaluation.victor.planning import plan
from connect_four.envs import TwoPlayerGameEnvVariables


def env_to_plan(env_variables: TwoPlayerGameEnvVariables) -> plan.Plan:
    board = Board(env_variables=env_variables)
    evaluation = evaluator.evaluate(board=board)
    if evaluation is None:
        raise ValueError("No solution for ", env_variables)

    plan_initializer = PlanInitializer(board=board, evaluation=evaluation)
    return plan_initializer.to_plan()


class PlanWrapper:
    def __init__(self, env):
        self.env = copy.deepcopy(env)
        self.plan = env_to_plan(self.env.env_variables)

    def execute(self, last_action) -> int:
        board = Board(self.env.env_variables)
        last_square = board.playable_square(last_action)
        responding_square = self.plan.execute(square=last_square)
        responding_action = responding_square.col

        # Move the internal model to the next step.
        self.env.step(last_action)
        self.env.step(responding_action)

        return responding_action


class PlanInitializer:
    def __init__(self, board: Board, evaluation: evaluator.Evaluation):
        self.rule_applications = set()
        self.availabilities = board.empty_squares()
        for solution in evaluation.chosen_set:
            self.rule_applications.add(solution.rule_instance)
            self.availabilities.difference_update(solution.squares)

        self.odd_group_guarantor = evaluation.odd_threat_guarantor
        squares_in_odd_group_guarantor_columns = set()
        if evaluation.odd_threat_guarantor is not None:
            for square in self.availabilities:
                if square.col in self.odd_group_guarantor.columns():
                    squares_in_odd_group_guarantor_columns.add(square)
        self.availabilities.difference_update(squares_in_odd_group_guarantor_columns)
        self.directly_playable_squares = board.playable_squares()

    def to_plan(self) -> plan.Plan:
        return plan.Plan(
            rule_applications=self.rule_applications,
            odd_group_guarantor=self.odd_group_guarantor,
            availabilities=self.availabilities,
            directly_playable_squares=self.directly_playable_squares,
        )
