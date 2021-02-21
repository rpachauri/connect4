from connect_four.agents.victor.game import Board
from connect_four.agents.victor.evaluator import evaluator
from connect_four.agents.victor.planning import plan
from connect_four.envs import ConnectFourEnvVariables


def env_to_plan(env_variables: ConnectFourEnvVariables) -> plan.Plan:
    board = Board(env_variables=env_variables)
    evaluation = evaluator.evaluate(board=board)
    if evaluation is None:
        raise ValueError("No solution for ", env_variables)

    plan_initializer = PlanInitializer(board=board, evaluation=evaluation)
    return plan_initializer.to_plan()


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
