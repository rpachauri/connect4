import unittest


from connect_four.agents.victor import Rule
from connect_four.agents.victor import Solution
from connect_four.agents.victor import Square

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
        self.assertTrue(combination.allowed_with_claimeven(
            solution=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
                threats=frozenset(),
            ),
            other=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=3, col=4),  # e3
                    Square(row=2, col=4),  # e4
                ]),
                threats=frozenset(),
            ),
        ))

        # Two Claimevens which cannot be combined.
        self.assertFalse(combination.allowed_with_claimeven(
            solution=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
                threats=frozenset(),
            ),
            other=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
                threats=frozenset(),
            ),
        ))

    def test_baseinverse_allowed_with_claimeven(self):
        # For this test:
        # solution is a Claimeven.
        # other is a Baseinverse.

        # A Baseinverse which can be combined with a Claimeven.
        self.assertTrue(combination.allowed_with_claimeven(
            solution=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
                threats=frozenset(),
            ),
            other=Solution(
                rule=Rule.Baseinverse,
                squares=frozenset([
                    Square(row=5, col=3),  # d1
                    Square(row=5, col=5),  # f1
                ]),
                threats=frozenset(),
            ),
        ))

        # A Baseinverse which cannot be combined with a Claimeven.
        self.assertFalse(combination.allowed_with_claimeven(
            solution=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
                threats=frozenset(),
            ),
            other=Solution(
                rule=Rule.Baseinverse,
                squares=frozenset([
                    Square(row=5, col=3),  # d1
                    Square(row=5, col=4),  # e1
                ]),
                threats=frozenset(),
            ),
        ))

    def test_vertical_allowed_with_claimeven(self):
        # For this test:
        # solution is a Claimeven.
        # other is a Vertical.

        # A Vertical which can be combined with a Claimeven.
        self.assertTrue(combination.allowed_with_claimeven(
            solution=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
                threats=frozenset(),
            ),
            other=Solution(
                rule=Rule.Vertical,
                squares=frozenset([
                    Square(row=4, col=3),  # d2
                    Square(row=3, col=3),  # d3
                ]),
                threats=frozenset(),
            ),
        ))

        # A Vertical which cannot be combined with a Claimeven.
        self.assertFalse(combination.allowed_with_claimeven(
            solution=Solution(
                rule=Rule.Claimeven,
                squares=frozenset([
                    Square(row=5, col=4),  # e1
                    Square(row=4, col=4),  # e2
                ]),
                threats=frozenset(),
            ),
            other=Solution(
                rule=Rule.Vertical,
                squares=frozenset([
                    Square(row=4, col=4),  # e2
                    Square(row=3, col=4),  # e3
                ]),
                threats=frozenset(),
            ),
        ))


if __name__ == '__main__':
    unittest.main()
