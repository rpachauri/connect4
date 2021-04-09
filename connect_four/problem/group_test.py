import unittest

from connect_four.game import Square
from connect_four.problem import Group
from connect_four.problem import GroupDirection


class TestGroup(unittest.TestCase):
    def test_player_validation(self):
        raises = False
        try:
            Group(player=-1, start=Square(0, 0), end=Square(3, 3))
        except ValueError:
            raises = True
        self.assertTrue(raises)

    def test_group_line_validation(self):
        raises = False
        try:
            Group(player=1, start=Square(0, 0), end=Square(1, 1))
        except ValueError:
            raises = True
        self.assertTrue(raises)

    def test_valid_group(self):
        Group(player=1, start=Square(0, 0), end=Square(3, 3))

    def test_equal(self):
        self.assertEqual(
            Group(player=1, start=Square(0, 0), end=Square(3, 3)),
            Group(player=1, start=Square(3, 3), end=Square(0, 0)),
        )
        self.assertNotEqual(
            Group(player=0, start=Square(0, 0), end=Square(3, 3)),
            Group(player=1, start=Square(3, 3), end=Square(0, 0)),
        )

    def test_group_direction(self):
        # Horizontal groups.
        self.assertEqual(GroupDirection.horizontal,
                         Group(player=1, start=Square(0, 0), end=Square(0, 3)).direction)
        self.assertEqual(GroupDirection.horizontal,
                         Group(player=1, start=Square(0, 3), end=Square(0, 0)).direction)
        # Up-left diagonal groups.
        self.assertEqual(GroupDirection.up_left_diagonal,
                         Group(player=1, start=Square(0, 0), end=Square(3, 3)).direction)
        self.assertEqual(GroupDirection.up_left_diagonal,
                         Group(player=1, start=Square(3, 3), end=Square(0, 0)).direction)
        # Vertical groups.
        self.assertEqual(GroupDirection.vertical,
                         Group(player=1, start=Square(0, 0), end=Square(3, 0)).direction)
        self.assertEqual(GroupDirection.vertical,
                         Group(player=1, start=Square(3, 0), end=Square(0, 0)).direction)
        # Up-right diagonal groups.
        self.assertEqual(GroupDirection.up_right_diagonal,
                         Group(player=1, start=Square(0, 3), end=Square(3, 0)).direction)
        self.assertEqual(GroupDirection.up_right_diagonal,
                         Group(player=1, start=Square(3, 0), end=Square(0, 3)).direction)


if __name__ == '__main__':
    unittest.main()
