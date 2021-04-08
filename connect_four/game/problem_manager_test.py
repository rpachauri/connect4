import unittest

from connect_four.game.data_structures import Group, Square
from connect_four.game.problem_manager import ProblemManager


class TestProblemManager(unittest.TestCase):
    def test_create_all_groups_3x3_num_to_connect_3(self):
        want_all_groups = {
            Group(squares=frozenset([Square(row=0, col=0), Square(row=0, col=1), Square(row=0, col=2)])),
            Group(squares=frozenset([Square(row=1, col=0), Square(row=1, col=1), Square(row=1, col=2)])),
            Group(squares=frozenset([Square(row=2, col=0), Square(row=2, col=1), Square(row=2, col=2)])),
            Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=0), Square(row=2, col=0)])),
            Group(squares=frozenset([Square(row=0, col=1), Square(row=1, col=1), Square(row=2, col=1)])),
            Group(squares=frozenset([Square(row=0, col=2), Square(row=1, col=2), Square(row=2, col=2)])),
            Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=1), Square(row=2, col=2)])),
            Group(squares=frozenset([Square(row=2, col=0), Square(row=1, col=1), Square(row=0, col=2)])),
        }
        got_all_groups = ProblemManager._create_all_groups(num_rows=3, num_cols=3, num_to_connect=3)
        self.assertEqual(want_all_groups, got_all_groups)

    def test_create_all_groups_6x7_num_to_connect_4(self):
        got_all_groups = ProblemManager._create_all_groups(num_rows=6, num_cols=7, num_to_connect=4)
        self.assertEqual(69, len(got_all_groups))

    def test_create_all_groups_by_square_by_player_3x3_num_to_connect_3(self):
        all_groups = ProblemManager._create_all_groups(num_rows=3, num_cols=3, num_to_connect=3)
        got_all_groups_by_square_by_player = ProblemManager._create_all_groups_by_square_by_player(
            num_rows=3,
            num_cols=3,
            all_groups=all_groups,
        )
        # There should be 2 players.
        self.assertEqual(2, len(got_all_groups_by_square_by_player))
        # For both players, there should be 3 rows.
        self.assertEqual(3, len(got_all_groups_by_square_by_player[0]))
        self.assertEqual(3, len(got_all_groups_by_square_by_player[1]))
        # For both players, there should be 3 cols.
        self.assertEqual(3, len(got_all_groups_by_square_by_player[0][0]))
        self.assertEqual(3, len(got_all_groups_by_square_by_player[1][0]))
        # Square 00 should have 3 groups for both players.
        self.assertEqual(3, len(got_all_groups_by_square_by_player[0][0][0]))
        self.assertEqual(3, len(got_all_groups_by_square_by_player[1][0][0]))
        # Square 01 should have 2 groups for both players.
        self.assertEqual(2, len(got_all_groups_by_square_by_player[0][0][1]))
        self.assertEqual(2, len(got_all_groups_by_square_by_player[1][0][1]))
        # Square 11 should have 4 groups for both players.
        self.assertEqual(4, len(got_all_groups_by_square_by_player[0][1][1]))
        self.assertEqual(4, len(got_all_groups_by_square_by_player[1][1][1]))


if __name__ == '__main__':
    unittest.main()
