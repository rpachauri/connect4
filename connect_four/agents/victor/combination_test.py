import unittest


from connect_four.agents.victor.rules import Rule
from connect_four.agents.victor import Solution
from connect_four.agents.victor.game import Square

from connect_four.agents.victor import combination


class TestCombination(unittest.TestCase):
    """Note that the combination module only cares about the set of Squares and
    the type of Rule of two Solutions. The module is not concerned with which Threats
    each Solution refutes.

    For this reason, Solutions in this module will have an empty set of threats.
    We want to emphasize that this is not normal but also not important for this module.

    In addition, it also doesn't matter what the board looks like. We can make any sort of
    assumptions about what the board looks like. This allows us to design interesting
    test cases without the restraints of creating a realistic board.
    """

    def test_claimeven_allowed_with_claimeven(self):
        # For this test:
        # solution is a Claimeven
        # other is a Claimeven.

        # Two Claimevens which can be combined.
        self.assertTrue(combination.allowed(
            s1=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
            ),
            s2=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=3, col=4),  # e3
                    Square(row=2, col=4),  # e4
                ]),
            ),
        ))

        # Two Claimevens which cannot be combined.
        self.assertFalse(combination.allowed(
            s1=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
            ),
            s2=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
            ),
        ))

    def test_baseinverse_allowed_with_claimeven(self):
        # For this test:
        # solution is a Claimeven.
        # other is a Baseinverse.

        # A Baseinverse which can be combined with a Claimeven.
        self.assertTrue(combination.allowed(
            s1=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
            ),
            s2=Solution(
                rule=Rule.Baseinverse,
                squares=frozenset([
                    Square(row=5, col=3),  # d1
                    Square(row=5, col=5),  # f1
                ]),
            ),
        ))

        # A Baseinverse which cannot be combined with a Claimeven.
        self.assertFalse(combination.allowed(
            s1=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
            ),
            s2=Solution(
                rule=Rule.Baseinverse,
                squares=frozenset([
                    Square(row=5, col=3),  # d1
                    Square(row=5, col=4),  # e1
                ]),
            ),
        ))

    def test_vertical_allowed_with_claimeven(self):
        # For this test:
        # solution is a Claimeven.
        # other is a Vertical.

        # A Vertical which can be combined with a Claimeven.
        self.assertTrue(combination.allowed(
            s1=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
            ),
            s2=Solution(
                rule=Rule.Vertical,
                squares=frozenset([
                    Square(row=4, col=3),  # d2
                    Square(row=3, col=3),  # d3
                ]),
            ),
        ))

        # A Vertical which cannot be combined with a Claimeven.
        self.assertFalse(combination.allowed(
            s1=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
            ),
            s2=Solution(
                rule=Rule.Vertical,
                squares=frozenset([
                    Square(row=4, col=4),  # e2
                    Square(row=3, col=4),  # e3
                ]),
            ),
        ))

    def test_lowinverse_allowed_with_claimeven(self):
        # For this test:
        # solution is a Claimeven.
        # other is a Lowinverse.

        # See Section 7.1 of the original paper for reasoning.
        # A Lowinverse which can be combined with a Claimeven.
        self.assertTrue(combination.allowed(
            s1=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=1, col=0),  # a5
                    Square(row=0, col=0),  # a6
                ]),
                claimeven_bottom_squares=[
                    Square(row=1, col=0),  # a5
                ],
            ),
            s2=Solution(
                rule=Rule.Lowinverse,
                squares=frozenset([
                    Square(row=4, col=0),  # a2
                    Square(row=3, col=0),  # a3
                    Square(row=4, col=1),  # b2
                    Square(row=3, col=1),  # b3
                ]),
            ),
        ))

        # See Diagram 7.2 from the original paper for an explanation.
        # A Lowinverse which cannot be combined with a Claimeven.
        self.assertFalse(combination.allowed(
            s1=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=0),  # a1
                    Square(row=4, col=0),  # a2
                ]),
                claimeven_bottom_squares=[
                    Square(row=5, col=0),  # a1
                ],
            ),
            s2=Solution(
                rule=Rule.Lowinverse,
                squares=frozenset([
                    Square(row=2, col=0),  # a4
                    Square(row=1, col=0),  # a5
                    Square(row=2, col=1),  # b4
                    Square(row=1, col=1),  # b5
                ]),
            ),
        ))

    def test_aftereven_allowed_with_aftereven(self):
        # For this test:
        # solution is an Aftereven.
        # other is an Aftereven.

        # Two Afterevens which can be combined.
        self.assertTrue(combination.allowed(
            s1=Solution(
                rule=Rule.Aftereven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                    Square(row=3, col=2),  # c3
                    Square(row=2, col=2),  # c4
                ]),
            ),
            s2=Solution(
                rule=Rule.Aftereven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                    Square(row=3, col=6),  # f3
                    Square(row=2, col=6),  # f4
                ]),
            ),
        ))


if __name__ == '__main__':
    unittest.main()
