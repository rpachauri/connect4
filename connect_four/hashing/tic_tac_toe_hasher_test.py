import unittest

from connect_four.hashing import TicTacToeHasher
from connect_four.hashing.tic_tac_toe_hasher import Square
from connect_four.hashing.tic_tac_toe_hasher import Group
from connect_four.hashing.tic_tac_toe_hasher import SquareType


class TestTicTacToeHasher(unittest.TestCase):
    GROUP_00_TO_02 = Group(squares=frozenset([Square(row=0, col=0), Square(row=0, col=1), Square(row=0, col=2)]))
    GROUP_10_TO_12 = Group(squares=frozenset([Square(row=1, col=0), Square(row=1, col=1), Square(row=1, col=2)]))
    GROUP_20_TO_22 = Group(squares=frozenset([Square(row=2, col=0), Square(row=2, col=1), Square(row=2, col=2)]))
    GROUP_00_TO_20 = Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=0), Square(row=2, col=0)]))
    GROUP_01_TO_21 = Group(squares=frozenset([Square(row=0, col=1), Square(row=1, col=1), Square(row=2, col=1)]))
    GROUP_02_TO_22 = Group(squares=frozenset([Square(row=0, col=2), Square(row=1, col=2), Square(row=2, col=2)]))
    GROUP_00_TO_22 = Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=1), Square(row=2, col=2)]))
    GROUP_20_TO_02 = Group(squares=frozenset([Square(row=2, col=0), Square(row=1, col=1), Square(row=0, col=2)]))

    def setUp(self) -> None:
        self.hasher = TicTacToeHasher()

    def test_init(self):
        # Validate expected groups.
        want_player_0_groups_at_00 = {
            TestTicTacToeHasher.GROUP_00_TO_02,
            TestTicTacToeHasher.GROUP_00_TO_22,
            TestTicTacToeHasher.GROUP_00_TO_20,
        }
        got_player_0_groups_at_00 = self.hasher.groups_by_squares[0][0][0]
        self.assertEqual(want_player_0_groups_at_00, got_player_0_groups_at_00)

        want_player_0_groups_at_11 = {
            TestTicTacToeHasher.GROUP_00_TO_22,
            TestTicTacToeHasher.GROUP_01_TO_21,
            TestTicTacToeHasher.GROUP_10_TO_12,
            TestTicTacToeHasher.GROUP_20_TO_02,
        }
        got_player_0_groups_at_11 = self.hasher.groups_by_squares[0][1][1]
        self.assertEqual(want_player_0_groups_at_11, got_player_0_groups_at_11)

        # Validate expected square types.
        self.assertEqual(SquareType.Empty, self.hasher.square_types[0][0])

        # Validate current player.
        self.assertEqual(0, self.hasher.player)


if __name__ == '__main__':
    unittest.main()
