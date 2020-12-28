import unittest

from connect_four.agents.victor import Square
from connect_four.agents.victor import Threat
from connect_four.agents.victor import ThreatDirection


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

    def test_threat_direction(self):
        # Horizontal threats.
        self.assertEqual(ThreatDirection.horizontal,
                         Threat(player=1, start=Square(0, 0), end=Square(0, 3)).direction)
        self.assertEqual(ThreatDirection.horizontal,
                         Threat(player=1, start=Square(0, 3), end=Square(0, 0)).direction)
        # Up-left diagonal threats.
        self.assertEqual(ThreatDirection.up_left_diagonal,
                         Threat(player=1, start=Square(0, 0), end=Square(3, 3)).direction)
        self.assertEqual(ThreatDirection.up_left_diagonal,
                         Threat(player=1, start=Square(3, 3), end=Square(0, 0)).direction)
        # Vertical threats.
        self.assertEqual(ThreatDirection.vertical,
                         Threat(player=1, start=Square(0, 0), end=Square(3, 0)).direction)
        self.assertEqual(ThreatDirection.vertical,
                         Threat(player=1, start=Square(3, 0), end=Square(0, 0)).direction)
        # Up-right diagonal threats.
        self.assertEqual(ThreatDirection.up_right_diagonal,
                         Threat(player=1, start=Square(0, 3), end=Square(3, 0)).direction)
        self.assertEqual(ThreatDirection.up_right_diagonal,
                         Threat(player=1, start=Square(3, 0), end=Square(0, 3)).direction)


if __name__ == '__main__':
    unittest.main()
