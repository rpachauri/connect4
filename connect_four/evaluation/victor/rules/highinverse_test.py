import gym
import unittest

import numpy as np

from connect_four.evaluation.victor.rules.highinverse import HighinverseManager, HighinverseColumn, \
    highinverses_given_column
from connect_four.game import Square
from connect_four.evaluation.board import Board

from connect_four.evaluation.victor.rules import Highinverse
from connect_four.evaluation.victor.rules import find_all_highinverses_using_highinverse_columns

from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.problem import Group
from connect_four.problem import ConnectFourGroupManager


class TestHighinverse(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_find_problems_solved_for_player_using_highinverse_columns(self):
        # This board is from Diagram 6.6 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        pm = ConnectFourGroupManager(env_variables=self.env.env_variables)

        # Highinverse c2-c3-c4-e2-e3-e4 guarantees at least one square
        # out of each pairs of squares:
        # 1. The upper two squares in the first column (c3-c4).
        # 2. The upper two squares in the second column (e3-e4).
        # 3. The middle squares from both columns (c3-e3).
        # 4. The upper squares from both columns (c4-e4).
        # 5. The lower square in the first column (since it's directly playable) and
        #    the upper square in the second column (c2-e4).
        # 6. The lower square in the second column (since it's directly playable) and
        #    the upper square in the first column (c4-e2).
        highinverse_c2_c3_c4_e2_e3_e4 = Highinverse(
            columns={
                HighinverseColumn(
                    upper=Square(row=2, col=2),  # c4
                    middle=Square(row=3, col=2),  # c3
                    lower=Square(row=4, col=2),  # c2
                    directly_playable=True,
                ),
                HighinverseColumn(
                    upper=Square(row=2, col=4),  # e4
                    middle=Square(row=3, col=4),  # e3
                    lower=Square(row=4, col=4),  # e2
                    directly_playable=True,
                ),
            }
        )

        want_problems_solved_for_player_0 = {
            # Groups solved by c3-c4.
            Group(player=0, start=Square(row=1, col=2), end=Square(row=4, col=2)),  # c2-c5
            Group(player=0, start=Square(row=0, col=2), end=Square(row=3, col=2)),  # c3-c6
            # Groups solved by e3-e4.
            Group(player=0, start=Square(row=2, col=4), end=Square(row=5, col=4)),  # e1-e4
            Group(player=0, start=Square(row=1, col=4), end=Square(row=4, col=4)),  # e2-e5
            Group(player=0, start=Square(row=0, col=4), end=Square(row=3, col=4)),  # e3-e6
            # Groups solved by c3-e3.
            Group(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
            Group(player=0, start=Square(row=3, col=2), end=Square(row=3, col=5)),  # c3-f3
            # Groups solved by c4-e4.
            Group(player=0, start=Square(row=2, col=1), end=Square(row=2, col=4)),  # b4-e4
            Group(player=0, start=Square(row=2, col=2), end=Square(row=2, col=5)),  # c4-f4
            # Groups solved by c2-e4.
            Group(player=0, start=Square(row=5, col=1), end=Square(row=2, col=4)),  # b1-e4
            Group(player=0, start=Square(row=4, col=2), end=Square(row=1, col=5)),  # c2-f5
            # Groups solved by c4-e2.
            Group(player=0, start=Square(row=1, col=1), end=Square(row=4, col=4)),  # b5-e2
            Group(player=0, start=Square(row=2, col=2), end=Square(row=5, col=5)),  # c4-f1
        }

        got_problems_solved_for_player_0 = highinverse_c2_c3_c4_e2_e3_e4.find_problems_solved_for_player(
            groups_by_square=pm.groups_by_square_by_player[0],
        )
        self.assertEqual(want_problems_solved_for_player_0, got_problems_solved_for_player_0)

    def test_diagram_7_2_using_highinverse_columns(self):
        # This test case is based on Diagram 7.2 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 1, 1, ],
                [0, 0, 1, 1, 0, 1, 0, ],
                [0, 0, 0, 0, 1, 1, 1, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 1, 0, ],
            ],
            [
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 1, 1, ],
                [0, 0, 0, 0, 1, 1, 0, ],
                [0, 1, 1, 0, 0, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)

        highinverse_column_a4_a5_a6 = HighinverseColumn(
            upper=Square(row=0, col=0),  # a6
            middle=Square(row=1, col=0),  # a5
            lower=Square(row=2, col=0),  # a4
            directly_playable=False,
        )
        highinverse_column_a2_a3_a4 = HighinverseColumn(
            upper=Square(row=2, col=0),  # a4
            middle=Square(row=3, col=0),  # a3
            lower=Square(row=4, col=0),  # a2
            directly_playable=False,
        )
        highinverse_column_b4_b5_b6 = HighinverseColumn(
            upper=Square(row=0, col=1),  # b6
            middle=Square(row=1, col=1),  # b5
            lower=Square(row=2, col=1),  # b4
            directly_playable=True,
        )

        want_highinverses = {
            Highinverse(columns={highinverse_column_a4_a5_a6, highinverse_column_b4_b5_b6}),
            Highinverse(columns={highinverse_column_a2_a3_a4, highinverse_column_b4_b5_b6}),
        }
        got_highinverses = find_all_highinverses_using_highinverse_columns(
            board=board,
        )
        self.assertEqual(want_highinverses, got_highinverses)

    def test_diagram_7_2_highinverse_manager_initialization(self):
        # This test case is based on Diagram 7.2 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 1, 1, ],
                [0, 0, 1, 1, 0, 1, 0, ],
                [0, 0, 0, 0, 1, 1, 1, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 1, 0, ],
            ],
            [
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 1, 1, ],
                [0, 0, 0, 0, 1, 1, 0, ],
                [0, 1, 1, 0, 0, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)
        hm = HighinverseManager(
            board=board,
        )
        got_highinverses = hm.highinverses

        highinverse_column_a4_a5_a6 = HighinverseColumn(
            upper=Square(row=0, col=0),  # a6
            middle=Square(row=1, col=0),  # a5
            lower=Square(row=2, col=0),  # a4
            directly_playable=False,
        )
        highinverse_column_a2_a3_a4 = HighinverseColumn(
            upper=Square(row=2, col=0),  # a4
            middle=Square(row=3, col=0),  # a3
            lower=Square(row=4, col=0),  # a2
            directly_playable=False,
        )
        highinverse_column_b4_b5_b6 = HighinverseColumn(
            upper=Square(row=0, col=1),  # b6
            middle=Square(row=1, col=1),  # b5
            lower=Square(row=2, col=1),  # b4
            directly_playable=True,
        )

        want_highinverses = {
            Highinverse(columns={highinverse_column_a4_a5_a6, highinverse_column_b4_b5_b6}),
            Highinverse(columns={highinverse_column_a2_a3_a4, highinverse_column_b4_b5_b6}),
        }
        self.assertEqual(want_highinverses, got_highinverses)

    def test_move_odd_square(self):
        # This test case is based on Diagram 7.2 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 1, 1, ],
                [0, 0, 1, 1, 0, 1, 0, ],
                [0, 0, 0, 0, 1, 1, 1, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 1, 0, ],
            ],
            [
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 1, 1, ],
                [0, 0, 0, 0, 1, 1, 0, ],
                [0, 1, 1, 0, 0, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)
        hm = HighinverseManager(
            board=board,
        )

        # When a1 is played, a2 becomes directly playable.
        old_highinverse_column_a2_a3_a4 = HighinverseColumn(
            upper=Square(row=2, col=0),  # a4
            middle=Square(row=3, col=0),  # a3
            lower=Square(row=4, col=0),  # a2
            directly_playable=False,
        )
        new_highinverse_column_a2_a3_a4 = HighinverseColumn(
            upper=Square(row=2, col=0),  # a4
            middle=Square(row=3, col=0),  # a3
            lower=Square(row=4, col=0),  # a2
            directly_playable=True,
        )
        highinverse_column_b4_b5_b6 = HighinverseColumn(
            upper=Square(row=0, col=1),  # b6
            middle=Square(row=1, col=1),  # b5
            lower=Square(row=2, col=1),  # b4
            directly_playable=True,
        )

        want_removed_highinverses = {
            Highinverse(columns={old_highinverse_column_a2_a3_a4, highinverse_column_b4_b5_b6}),
        }
        want_added_highinverses = {
            Highinverse(columns={new_highinverse_column_a2_a3_a4, highinverse_column_b4_b5_b6}),
        }
        got_removed_highinverses, got_added_highinverses = hm.move(square=Square(row=5, col=0))

        self.assertEqual(want_removed_highinverses, got_removed_highinverses)
        self.assertEqual(want_added_highinverses, got_added_highinverses)

    def test_solves_using_highinverse_columns(self):
        # Highinverse c2-c3-c4-e2-e3-e4 guarantees at least one square
        # out of each pairs of squares:
        # 1. The upper two squares in the first column (c3-e4).
        # 2. The upper two squares in the second column (d3-e4).
        # 3. The middle squares from both columns (c3-e3).
        # 4. The upper squares from both columns (c4-e4).
        # 5. The lower square in the first column (since it's directly playable) and
        #    the upper square in the second column.
        # 6. The lower square in the second column (since it's directly playable) and
        #    the upper square in the first column.
        highinverse_c2_c3_c4_e2_e3_e4 = Highinverse(
            columns={
                HighinverseColumn(
                    upper=Square(row=2, col=2),  # c4
                    middle=Square(row=3, col=2),  # c3
                    lower=Square(row=4, col=2),  # c2
                    directly_playable=True,
                ),
                HighinverseColumn(
                    upper=Square(row=2, col=4),  # e4
                    middle=Square(row=3, col=4),  # e3
                    lower=Square(row=4, col=4),  # e2
                    directly_playable=True,
                ),
            }
        )

        # Group which contain the upper squares of both columns.
        white_group_b4_e4 = Group(player=0, start=Square(row=2, col=1), end=Square(row=2, col=4))  # b4-e4
        self.assertTrue(highinverse_c2_c3_c4_e2_e3_e4.solves(group=white_group_b4_e4))
        # Group which contain the middle squares of both columns.
        white_group_b3_e3 = Group(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4))  # b3-e3
        self.assertTrue(highinverse_c2_c3_c4_e2_e3_e4.solves(group=white_group_b3_e3))
        # Group that can be refuted by Vertical c3-c4.
        white_group_c3_c6 = Group(player=0, start=Square(row=0, col=2), end=Square(row=3, col=2))  # c3-c6
        self.assertTrue(highinverse_c2_c3_c4_e2_e3_e4.solves(group=white_group_c3_c6))
        # Group that can be refuted by Vertical e3-e4.
        white_group_e3_e6 = Group(player=0, start=Square(row=0, col=4), end=Square(row=3, col=4))  # e3-e6
        self.assertTrue(highinverse_c2_c3_c4_e2_e3_e4.solves(group=white_group_e3_e6))
        # Group that can be refuted by c2-e4.
        white_group_c2_f5 = Group(player=0, start=Square(row=4, col=2), end=Square(row=1, col=5))  # c2-f5
        self.assertTrue(highinverse_c2_c3_c4_e2_e3_e4.solves(group=white_group_c2_f5))
        # Group that can be refuted by c4-e2.
        white_group_c4_f1 = Group(player=0, start=Square(row=2, col=2), end=Square(row=5, col=5))  # c4-f1
        self.assertTrue(highinverse_c2_c3_c4_e2_e3_e4.solves(group=white_group_c4_f1))
        # Group that cannot be solved by the Highinverse at all.
        white_group_a5_d6 = Group(player=0, start=Square(row=1, col=0), end=Square(row=1, col=3))  # a5-d5
        self.assertFalse(highinverse_c2_c3_c4_e2_e3_e4.solves(group=white_group_a5_d6))

    def test_is_useful_using_highinverse_columns(self):
        highinverse_c2_c3_c4_e2_e3_e4 = Highinverse(
            columns={
                HighinverseColumn(
                    upper=Square(row=2, col=2),  # c4
                    middle=Square(row=3, col=2),  # c3
                    lower=Square(row=4, col=2),  # c2
                    directly_playable=True,
                ),
                HighinverseColumn(
                    upper=Square(row=2, col=4),  # e4
                    middle=Square(row=3, col=4),  # e3
                    lower=Square(row=4, col=4),  # e2
                    directly_playable=True,
                ),
            }
        )

        # Highinverse is useful as long as it solves a single group.
        white_group_a4_d4 = Group(player=0, start=Square(row=2, col=0), end=Square(row=2, col=3))  # a4-d4
        self.assertTrue(highinverse_c2_c3_c4_e2_e3_e4.is_useful(groups={white_group_a4_d4}))
        self.assertFalse(highinverse_c2_c3_c4_e2_e3_e4.is_useful(groups=set()))

    def test_highinverses_given_column_connection_possible_between_two_upper_and_middle_squares(self):
        highinverse_column_a4_a5_a6 = HighinverseColumn(
            upper=Square(row=0, col=0),  # a6
            middle=Square(row=1, col=0),  # a5
            lower=Square(row=2, col=0),  # a4
            directly_playable=False,
        )

        # Connection is possible between the two upper and middle squares.
        highinverse_column_b4_b5_b6 = HighinverseColumn(
            upper=Square(row=0, col=1),  # b6
            middle=Square(row=1, col=1),  # b5
            lower=Square(row=2, col=1),  # b4
            directly_playable=False,
        )
        # Connection is not possible between the two upper and middle squares.
        highinverse_column_e4_e5_e6 = HighinverseColumn(
            upper=Square(row=0, col=4),  # e6
            middle=Square(row=1, col=4),  # e5
            lower=Square(row=2, col=4),  # e4
            directly_playable=False,
        )
        columns = {
            highinverse_column_b4_b5_b6,
            highinverse_column_e4_e5_e6,
        }
        want_highinverses = {
            Highinverse(
                columns={highinverse_column_a4_a5_a6, highinverse_column_b4_b5_b6},
            )
        }
        got_highinverses = highinverses_given_column(column=highinverse_column_a4_a5_a6, columns=columns)
        self.assertEqual(want_highinverses, got_highinverses)

    def test_highinverses_given_column_connection_possible_between_lower_and_upper_squares(self):
        # Test for when the lower square of one of the columns is directly playable and can be connected with the
        # upper square of the other column.
        highinverse_column_a4_a5_a6_not_playable = HighinverseColumn(
            upper=Square(row=0, col=0),  # a6
            middle=Square(row=1, col=0),  # a5
            lower=Square(row=2, col=0),  # a4
            directly_playable=False,
        )
        highinverse_column_a4_a5_a6_playable = HighinverseColumn(
            upper=Square(row=0, col=0),  # a6
            middle=Square(row=1, col=0),  # a5
            lower=Square(row=2, col=0),  # a4
            directly_playable=True,
        )
        highinverse_column_b4_b5_b6 = HighinverseColumn(
            upper=Square(row=2, col=1),  # b4
            middle=Square(row=3, col=1),  # b3
            lower=Square(row=4, col=1),  # b2
            directly_playable=False,
        )

        want_highinverses = {
            Highinverse(columns={highinverse_column_a4_a5_a6_playable, highinverse_column_b4_b5_b6}),
        }

        # Covers the case when column contains the directly playable square.
        columns_containing_the_b_column = {
            highinverse_column_b4_b5_b6,
        }
        got_highinverses = highinverses_given_column(
            column=highinverse_column_a4_a5_a6_playable,
            columns=columns_containing_the_b_column,
        )
        self.assertEqual(want_highinverses, got_highinverses)

        # Covers the case when other_column contains the directly playable square.
        columns_containing_the_a_column = {
            highinverse_column_a4_a5_a6_playable,
            highinverse_column_a4_a5_a6_not_playable,
        }
        got_highinverses = highinverses_given_column(
            column=highinverse_column_b4_b5_b6,
            columns=columns_containing_the_a_column,
        )
        self.assertEqual(want_highinverses, got_highinverses)


if __name__ == '__main__':
    unittest.main()
