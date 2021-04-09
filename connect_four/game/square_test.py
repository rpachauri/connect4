import unittest

from connect_four.game import Square


class TestSquare(unittest.TestCase):

    def test_equal(self):
        self.assertEqual(Square(2, 3), Square(2, 3))


if __name__ == '__main__':
    unittest.main()
