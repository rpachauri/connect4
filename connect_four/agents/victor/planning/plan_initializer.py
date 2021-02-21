from connect_four.agents.victor.game import Board
from connect_four.agents.victor.evaluator.evaluator import Evaluation


class PlanInitializer:
    def __init__(self, board: Board, evaluation: Evaluation):
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
