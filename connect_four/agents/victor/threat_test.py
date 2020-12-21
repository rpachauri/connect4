import unittest

from connect_four.agents.victor import Square
from connect_four.agents.victor import Threat


class TestThreat(unittest.TestCase):
    def test_player_validation(self):
        raises = False
        try:
            Threat(player=-1, start=Square(0, 0), end=Square(3, 3))
        except ValueError:
            raises = True
        self.assertTrue(raises)

    def test_threat_line_validation(self):
        raises = False
        try:
            Threat(player=1, start=Square(0, 0), end=Square(1, 1))
        except ValueError:
            raises = True
        self.assertTrue(raises)

    def test_valid_threat(self):
        Threat(player=1, start=Square(0, 0), end=Square(3, 3))

    def test_equal(self):
        self.assertEqual(
            Threat(player=1, start=Square(0, 0), end=Square(3, 3)),
            Threat(player=1, start=Square(3, 3), end=Square(0, 0)),
        )
        self.assertNotEqual(
            Threat(player=0, start=Square(0, 0), end=Square(3, 3)),
            Threat(player=1, start=Square(3, 3), end=Square(0, 0)),
        )


if __name__ == '__main__':
    unittest.main()
