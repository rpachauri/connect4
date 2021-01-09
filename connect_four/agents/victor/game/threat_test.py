import unittest

from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Threat
from connect_four.agents.victor.game import ThreatDirection
from connect_four.agents.victor.game.threat import create_square_to_threats


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

    def test_square_to_threats(self):
        threat = Threat(player=1, start=Square(0, 0), end=Square(3, 3))
        want_square_to_threats = {
            Square(0, 0): {threat},
            Square(1, 1): {threat},
            Square(2, 2): {threat},
            Square(3, 3): {threat},
        }
        got_square_to_threats = create_square_to_threats([threat])
        self.assertEqual(want_square_to_threats, got_square_to_threats)


if __name__ == '__main__':
    unittest.main()
