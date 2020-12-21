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


if __name__ == '__main__':
    unittest.main()
