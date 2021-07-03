import unittest

from connect_four.evaluation.victor.rules import connection
from connect_four.game import Square


class TestConnection(unittest.TestCase):
    def test_same_square(self):
        a = Square(row=0, col=0)
        b = Square(row=0, col=0)
        with self.assertRaises(ValueError):
            connection.is_possible(a=a, b=b)

    def test_row_diff_greater_than_3(self):
        a = Square(row=0, col=0)
        b = Square(row=4, col=0)
        self.assertFalse(connection.is_possible(a=a, b=b))

    def test_col_diff_greater_than_3(self):
        a = Square(row=0, col=0)
        b = Square(row=0, col=4)
        self.assertFalse(connection.is_possible(a=a, b=b))

    def test_same_row(self):
        a = Square(row=0, col=0)
        b = Square(row=0, col=3)
        self.assertTrue(connection.is_possible(a=a, b=b))

    def test_same_col(self):
        a = Square(row=0, col=0)
        b = Square(row=2, col=0)
        self.assertTrue(connection.is_possible(a=a, b=b))

    def test_left_diagonal(self):
        a = Square(row=0, col=0)
        b = Square(row=1, col=1)
        self.assertTrue(connection.is_possible(a=a, b=b))

    def test_right_diagonal(self):
        a = Square(row=2, col=2)
        b = Square(row=4, col=0)
        self.assertTrue(connection.is_possible(a=a, b=b))

    def test_impossible_left_diagonal(self):
        a = Square(row=4, col=0)
        b = Square(row=5, col=1)
        self.assertFalse(connection.is_possible(a=a, b=b))

    def test_impossible_right_diagonal(self):
        a = Square(row=0, col=1)
        b = Square(row=1, col=0)
        self.assertFalse(connection.is_possible(a=a, b=b))


if __name__ == '__main__':
    unittest.main()
