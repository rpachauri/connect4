import unittest

from connect_four.hashing.data_structures import Group, Square
from connect_four.hashing.square_type_manager import SquareTypeManager


class TestSquareTypeManager(unittest.TestCase):

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
        got_all_groups = SquareTypeManager._create_all_groups(num_rows=3, num_cols=3, num_to_connect=3)
        self.assertEqual(want_all_groups, got_all_groups)

    def test_create_all_groups_6x7_num_to_connect_4(self):
        got_all_groups = SquareTypeManager._create_all_groups(num_rows=6, num_cols=7, num_to_connect=4)
        self.assertEqual(69, len(got_all_groups))


if __name__ == '__main__':
    unittest.main()
