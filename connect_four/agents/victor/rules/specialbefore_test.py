import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Group

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Before
from connect_four.agents.victor.rules import find_all_befores
from connect_four.agents.victor.rules import Specialbefore
from connect_four.agents.victor.rules import find_all_specialbefores

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestSpecialbefore(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_unused_vertical(self):
        directly_playable_square_3_3 = Square(row=3, col=3)
        directly_playable_square_4_4 = Square(row=4, col=4)
        square_above_directly_playable_square_4_4 = Square(row=3, col=4)
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))
        group_4_3_to_4_6 = Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6))
        before_4_3_to_4_6 = Before(
            group=group_4_3_to_4_6,
            verticals=[vertical_3_4],
            claimevens=[],
        )
        specialbefore = Specialbefore(
            before=before_4_3_to_4_6,
            internal_directly_playable_square=directly_playable_square_4_4,
            external_directly_playable_square=directly_playable_square_3_3,
        )
        want_unused_vertical = Vertical(
            lower=directly_playable_square_4_4,
            upper=square_above_directly_playable_square_4_4,
        )
        got_unused_vertical = specialbefore.unused_vertical()
        self.assertEqual(want_unused_vertical, got_unused_vertical)

    def test_before_simplified_diagram_6_10(self):
        # This is a modified test case from Diagram 6.10 from the original paper.
        # We filled up a lot of the columns to simplify the test case and reduce the total number of Specialbefores.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [1, 0, 0, 0, 0, 1, 1, ],
                [0, 1, 1, 0, 0, 0, 0, ],
                [1, 0, 0, 0, 0, 1, 1, ],
                [0, 1, 1, 0, 0, 0, 0, ],
                [1, 0, 1, 1, 0, 1, 1, ],
            ],
            [
                [1, 0, 1, 0, 0, 1, 1, ],
                [0, 1, 1, 0, 0, 0, 0, ],
                [1, 0, 0, 0, 0, 1, 1, ],
                [0, 1, 1, 0, 0, 0, 0, ],
                [1, 0, 0, 1, 0, 1, 1, ],
                [0, 1, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        black_groups = board.potential_groups(player=1)
        befores = find_all_befores(board=board, opponent_groups=black_groups)
        got_specialbefores = find_all_specialbefores(board=board, befores=befores)

        # Directly playable squares.
        directly_playable_square_0_1 = Square(row=0, col=1)
        directly_playable_square_3_3 = Square(row=3, col=3)
        directly_playable_square_4_4 = Square(row=4, col=4)

        # Non-vertical groups for black that contain at least one directly playable square.
        group_3_1_to_3_4 = Group(player=1, start=Square(row=3, col=1), end=Square(row=3, col=4))
        group_4_3_to_4_6 = Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6))

        # Verticals/Claimevens that can belong to Befores.
        vertical_2_3 = Vertical(upper=Square(row=2, col=3), lower=Square(row=3, col=3))
        vertical_2_4 = Vertical(upper=Square(row=2, col=4), lower=Square(row=3, col=4))
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))

        before_3_1_to_3_4_variation_1 = Before(
            group=group_3_1_to_3_4,
            verticals=[vertical_2_3, vertical_2_4],
            claimevens=[],
        )
        before_3_1_to_3_4_variation_2 = Before(
            group=group_3_1_to_3_4,
            verticals=[vertical_2_3, vertical_3_4],
            claimevens=[],
        )
        before_4_3_to_4_6 = Before(
            group=group_4_3_to_4_6,
            verticals=[vertical_3_4],
            claimevens=[],
        )

        want_specialbefores = {
            # Specialbefores for before_3_1_to_3_4_variation_1.
            Specialbefore(
                before=before_3_1_to_3_4_variation_1,
                internal_directly_playable_square=directly_playable_square_3_3,
                external_directly_playable_square=directly_playable_square_0_1,
            ),
            # Specialbefores for before_3_1_to_3_4_variation_2.
            Specialbefore(
                before=before_3_1_to_3_4_variation_2,
                internal_directly_playable_square=directly_playable_square_3_3,
                external_directly_playable_square=directly_playable_square_0_1,
            ),
            # Specialbefores for before_4_3_to_4_6.
            Specialbefore(
                before=before_4_3_to_4_6,
                internal_directly_playable_square=directly_playable_square_4_4,
                external_directly_playable_square=directly_playable_square_0_1,
            ),
            Specialbefore(
                before=before_4_3_to_4_6,
                internal_directly_playable_square=directly_playable_square_4_4,
                external_directly_playable_square=directly_playable_square_3_3,
            ),
        }
        self.assertEqual(want_specialbefores, got_specialbefores)

    def test_before_diagram_6_10(self):
        # This test case tries to find all possible Specialbefores from Diagram 6.10 in the original paper.
        # The authors go through 1 example of a Specialbefore, but we find that there are in fact 216 possible
        # Specialbefores. Not all of them may be useful (i.e. refute any new groups); however,
        # they do satisfy the formal requirements as specified in the original paper.
        # This test case is quite obscene; however, it did help in finding a few bugs.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        black_groups = board.potential_groups(player=1)
        befores = find_all_befores(board=board, opponent_groups=black_groups)
        got_specialbefores = find_all_specialbefores(board=board, befores=befores)

        # Directly playable squares for the board.
        directly_playable_square_5_0 = Square(row=5, col=0)
        directly_playable_square_5_1 = Square(row=5, col=1)
        directly_playable_square_0_2 = Square(row=0, col=2)
        directly_playable_square_3_3 = Square(row=3, col=3)
        directly_playable_square_4_4 = Square(row=4, col=4)
        directly_playable_square_5_5 = Square(row=5, col=5)
        directly_playable_square_5_6 = Square(row=5, col=6)

        # groups for Black that meet the following conditions:
        # 1. Not vertical.
        # 2. Contain at least one directly playable square.
        # 3. Do not contain a square in the top row.
        ## groups for Black containing directly_playable_square_5_0.
        group_5_0_to_2_3 = Group(player=1, start=directly_playable_square_5_0, end=Square(row=2, col=3))
        ## groups for Black containing directly_playable_square_3_3.
        group_3_0_to_3_3 = Group(player=1, start=Square(row=3, col=0), end=directly_playable_square_3_3)
        group_3_1_to_3_4 = Group(player=1, start=Square(row=3, col=1), end=Square(row=3, col=4))
        group_3_2_to_3_5 = Group(player=1, start=Square(row=3, col=2), end=Square(row=3, col=5))
        group_3_3_to_3_6 = Group(player=1, start=directly_playable_square_3_3, end=Square(row=3, col=6))
        ## groups for Black containing directly_playable_square_4_4.
        group_4_3_to_4_6 = Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6))
        ## groups for Black containing directly_playable_square_5_6.
        group_2_3_to_5_6 = Group(player=1, start=Square(row=2, col=3), end=Square(row=5, col=6))

        # All Verticals/Claimevens used in all Before variations of the group (5, 0) to (2, 3).
        vertical_4_0 = Vertical(upper=Square(row=4, col=0), lower=Square(row=5, col=0))
        claimeven_4_1 = Claimeven(upper=Square(row=4, col=1), lower=Square(row=5, col=1))
        vertical_3_1 = Vertical(upper=Square(row=3, col=1), lower=Square(row=4, col=1))
        claimeven_2_3 = Claimeven(upper=Square(row=2, col=3), lower=Square(row=3, col=3))
        vertical_1_3 = Vertical(upper=Square(row=1, col=3), lower=Square(row=2, col=3))

        # All Before variations of the group (5, 0) to (2, 3).
        before_5_0_to_2_3_variation_1 = Before(
            group=group_5_0_to_2_3,
            verticals=[vertical_4_0],
            claimevens=[claimeven_4_1, claimeven_2_3]
        )
        before_5_0_to_2_3_variation_2 = Before(
            group=group_5_0_to_2_3,
            verticals=[vertical_4_0, vertical_1_3],
            claimevens=[claimeven_4_1]
        )
        before_5_0_to_2_3_variation_3 = Before(
            group=group_5_0_to_2_3,
            verticals=[vertical_4_0, vertical_3_1],
            claimevens=[claimeven_2_3]
        )
        before_5_0_to_2_3_variation_4 = Before(
            group=group_5_0_to_2_3,
            verticals=[vertical_4_0, vertical_3_1, vertical_1_3],
            claimevens=[]
        )

        # All Verticals/Claimevens used in all Before variations of the group (3, 0) to (3, 3).
        vertical_2_0 = Vertical(upper=Square(row=2, col=0), lower=Square(row=3, col=0))
        vertical_3_0 = Vertical(upper=Square(row=3, col=0), lower=Square(row=4, col=0))
        vertical_2_1 = Vertical(upper=Square(row=2, col=1), lower=Square(row=3, col=1))
        vertical_3_1 = Vertical(upper=Square(row=3, col=1), lower=Square(row=4, col=1))
        vertical_2_3 = Vertical(upper=Square(row=2, col=3), lower=Square(row=3, col=3))

        # All Before variations of the group (3, 0) to (3, 3).
        before_3_0_to_3_3_variation_1 = Before(
            group=group_3_0_to_3_3,
            verticals=[vertical_2_0, vertical_2_1, vertical_2_3],
            claimevens=[],
        )
        before_3_0_to_3_3_variation_2 = Before(
            group=group_3_0_to_3_3,
            verticals=[vertical_2_0, vertical_3_1, vertical_2_3],
            claimevens=[],
        )
        before_3_0_to_3_3_variation_3 = Before(
            group=group_3_0_to_3_3,
            verticals=[vertical_3_0, vertical_2_1, vertical_2_3],
            claimevens=[],
        )
        before_3_0_to_3_3_variation_4 = Before(
            group=group_3_0_to_3_3,
            verticals=[vertical_3_0, vertical_3_1, vertical_2_3],
            claimevens=[],
        )

        # All Verticals/Claimevens used in all Before variations of the group (3, 1) to (3, 4).
        vertical_2_1 = Vertical(upper=Square(row=2, col=1), lower=Square(row=3, col=1))
        vertical_3_1 = Vertical(upper=Square(row=3, col=1), lower=Square(row=4, col=1))
        vertical_2_3 = Vertical(upper=Square(row=2, col=3), lower=Square(row=3, col=3))
        vertical_2_4 = Vertical(upper=Square(row=2, col=4), lower=Square(row=3, col=4))
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))

        # All Before variations of the group (3, 1) to (3, 4).
        before_3_1_to_3_4_variation_1 = Before(
            group=group_3_1_to_3_4,
            verticals=[vertical_2_1, vertical_2_3, vertical_2_4],
            claimevens=[],
        )
        before_3_1_to_3_4_variation_2 = Before(
            group=group_3_1_to_3_4,
            verticals=[vertical_2_1, vertical_2_3, vertical_3_4],
            claimevens=[],
        )
        before_3_1_to_3_4_variation_3 = Before(
            group=group_3_1_to_3_4,
            verticals=[vertical_3_1, vertical_2_3, vertical_2_4],
            claimevens=[],
        )
        before_3_1_to_3_4_variation_4 = Before(
            group=group_3_1_to_3_4,
            verticals=[vertical_3_1, vertical_2_3, vertical_3_4],
            claimevens=[],
        )

        # All Verticals/Claimevens used in all Before variations of the group (3, 2) to (3, 5).
        vertical_2_3 = Vertical(upper=Square(row=2, col=3), lower=Square(row=3, col=3))
        vertical_2_4 = Vertical(upper=Square(row=2, col=4), lower=Square(row=3, col=4))
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))
        vertical_2_5 = Vertical(upper=Square(row=2, col=5), lower=Square(row=3, col=5))
        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))

        # All Before variations of the group (3, 2) to (3, 5).
        before_3_2_to_3_5_variation_1 = Before(
            group=group_3_2_to_3_5,
            verticals=[vertical_2_3, vertical_2_4, vertical_2_5],
            claimevens=[],
        )
        before_3_2_to_3_5_variation_2 = Before(
            group=group_3_2_to_3_5,
            verticals=[vertical_2_3, vertical_2_4, vertical_3_5],
            claimevens=[],
        )
        before_3_2_to_3_5_variation_3 = Before(
            group=group_3_2_to_3_5,
            verticals=[vertical_2_3, vertical_3_4, vertical_2_5],
            claimevens=[],
        )
        before_3_2_to_3_5_variation_4 = Before(
            group=group_3_2_to_3_5,
            verticals=[vertical_2_3, vertical_3_4, vertical_3_5],
            claimevens=[],
        )

        # All Verticals/Claimevens used in all Before variations of the group (3, 3) to (3, 6).
        vertical_2_3 = Vertical(upper=Square(row=2, col=3), lower=Square(row=3, col=3))
        vertical_2_4 = Vertical(upper=Square(row=2, col=4), lower=Square(row=3, col=4))
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))
        vertical_2_5 = Vertical(upper=Square(row=2, col=5), lower=Square(row=3, col=5))
        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        vertical_2_6 = Vertical(upper=Square(row=2, col=6), lower=Square(row=3, col=6))
        vertical_3_6 = Vertical(upper=Square(row=3, col=6), lower=Square(row=4, col=6))

        # All Before variations of the group (3, 3) to (3, 6).
        before_3_3_to_3_6_variation_1 = Before(
            group=group_3_3_to_3_6,
            verticals=[vertical_2_3, vertical_2_4, vertical_2_5, vertical_2_6],
            claimevens=[],
        )
        before_3_3_to_3_6_variation_2 = Before(
            group=group_3_3_to_3_6,
            verticals=[vertical_2_3, vertical_2_4, vertical_2_5, vertical_3_6],
            claimevens=[],
        )
        before_3_3_to_3_6_variation_3 = Before(
            group=group_3_3_to_3_6,
            verticals=[vertical_2_3, vertical_2_4, vertical_3_5, vertical_2_6],
            claimevens=[],
        )
        before_3_3_to_3_6_variation_4 = Before(
            group=group_3_3_to_3_6,
            verticals=[vertical_2_3, vertical_2_4, vertical_3_5, vertical_3_6],
            claimevens=[],
        )
        before_3_3_to_3_6_variation_5 = Before(
            group=group_3_3_to_3_6,
            verticals=[vertical_2_3, vertical_3_4, vertical_2_5, vertical_2_6],
            claimevens=[],
        )
        before_3_3_to_3_6_variation_6 = Before(
            group=group_3_3_to_3_6,
            verticals=[vertical_2_3, vertical_3_4, vertical_2_5, vertical_3_6],
            claimevens=[],
        )
        before_3_3_to_3_6_variation_7 = Before(
            group=group_3_3_to_3_6,
            verticals=[vertical_2_3, vertical_3_4, vertical_3_5, vertical_2_6],
            claimevens=[],
        )
        before_3_3_to_3_6_variation_8 = Before(
            group=group_3_3_to_3_6,
            verticals=[vertical_2_3, vertical_3_4, vertical_3_5, vertical_3_6],
            claimevens=[],
        )

        # All Verticals/Claimevens used in all Before variations of the group (4, 3) to (4, 6).
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))
        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        claimeven_4_5 = Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5))
        vertical_3_6 = Vertical(upper=Square(row=3, col=6), lower=Square(row=4, col=6))
        claimeven_4_6 = Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6))

        # All Before variations of the group (4, 3) to (4, 6).
        before_4_3_to_4_6_variation_1 = Before(
            group=group_4_3_to_4_6,
            verticals=[vertical_3_4, vertical_3_5, vertical_3_6],
            claimevens=[],
        )
        before_4_3_to_4_6_variation_2 = Before(
            group=group_4_3_to_4_6,
            verticals=[vertical_3_4, vertical_3_5],
            claimevens=[claimeven_4_6],
        )
        before_4_3_to_4_6_variation_3 = Before(
            group=group_4_3_to_4_6,
            verticals=[vertical_3_4, vertical_3_6],
            claimevens=[claimeven_4_5],
        )
        before_4_3_to_4_6_variation_4 = Before(
            group=group_4_3_to_4_6,
            verticals=[vertical_3_4],
            claimevens=[claimeven_4_5, claimeven_4_6],
        )

        # All Verticals/Claimevens used in all Before variations of the group (2, 3) to (5, 6).
        vertical_1_3 = Vertical(upper=Square(row=1, col=3), lower=Square(row=2, col=3))
        claimeven_2_3 = Claimeven(upper=Square(row=2, col=3), lower=Square(row=3, col=3))
        vertical_2_4 = Vertical(upper=Square(row=2, col=4), lower=Square(row=3, col=4))
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))
        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        claimeven_4_5 = Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5))
        vertical_4_6 = Vertical(upper=Square(row=4, col=6), lower=Square(row=5, col=6))

        # All Before variations of the group (2, 3) to (5, 6).
        before_2_3_to_5_6_variation_1 = Before(
            group=group_2_3_to_5_6,
            verticals=[vertical_1_3, vertical_2_4, vertical_3_5, vertical_4_6],
            claimevens=[],
        )
        before_2_3_to_5_6_variation_2 = Before(
            group=group_2_3_to_5_6,
            verticals=[vertical_1_3, vertical_2_4, vertical_4_6],
            claimevens=[claimeven_4_5],
        )
        before_2_3_to_5_6_variation_3 = Before(
            group=group_2_3_to_5_6,
            verticals=[vertical_1_3, vertical_3_4, vertical_3_5, vertical_4_6],
            claimevens=[],
        )
        before_2_3_to_5_6_variation_4 = Before(
            group=group_2_3_to_5_6,
            verticals=[vertical_1_3, vertical_3_4, vertical_4_6],
            claimevens=[claimeven_4_5],
        )
        before_2_3_to_5_6_variation_5 = Before(
            group=group_2_3_to_5_6,
            verticals=[vertical_2_4, vertical_3_5, vertical_4_6],
            claimevens=[claimeven_2_3],
        )
        before_2_3_to_5_6_variation_6 = Before(
            group=group_2_3_to_5_6,
            verticals=[vertical_2_4, vertical_4_6],
            claimevens=[claimeven_2_3, claimeven_4_5],
        )
        before_2_3_to_5_6_variation_7 = Before(
            group=group_2_3_to_5_6,
            verticals=[vertical_3_4, vertical_3_5, vertical_4_6],
            claimevens=[claimeven_2_3],
        )
        before_2_3_to_5_6_variation_8 = Before(
            group=group_2_3_to_5_6,
            verticals=[vertical_3_4, vertical_4_6],
            claimevens=[claimeven_2_3, claimeven_4_5],
        )

        want_specialbefores = {
            # All Specialbefores for before_5_0_to_2_3_variation_1.
            Specialbefore(before=before_5_0_to_2_3_variation_1,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_5_0_to_2_3_variation_1,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_4_4),
            Specialbefore(before=before_5_0_to_2_3_variation_1,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_5_0_to_2_3_variation_1,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_5_0_to_2_3_variation_2.
            Specialbefore(before=before_5_0_to_2_3_variation_2,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_5_0_to_2_3_variation_2,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_4_4),
            Specialbefore(before=before_5_0_to_2_3_variation_2,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_5_0_to_2_3_variation_2,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_5_0_to_2_3_variation_3.
            Specialbefore(before=before_5_0_to_2_3_variation_3,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_5_0_to_2_3_variation_3,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_4_4),
            Specialbefore(before=before_5_0_to_2_3_variation_3,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_5_0_to_2_3_variation_3,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_5_0_to_2_3_variation_4.
            Specialbefore(before=before_5_0_to_2_3_variation_4,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_5_0_to_2_3_variation_4,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_4_4),
            Specialbefore(before=before_5_0_to_2_3_variation_4,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_5_0_to_2_3_variation_4,
                          internal_directly_playable_square=directly_playable_square_5_0,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_0_to_3_3_variation_1.
            Specialbefore(before=before_3_0_to_3_3_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_0_to_3_3_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_4_4),
            Specialbefore(before=before_3_0_to_3_3_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_3_0_to_3_3_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_0_to_3_3_variation_2.
            Specialbefore(before=before_3_0_to_3_3_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_0_to_3_3_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_4_4),
            Specialbefore(before=before_3_0_to_3_3_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_3_0_to_3_3_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_0_to_3_3_variation_3.
            Specialbefore(before=before_3_0_to_3_3_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_0_to_3_3_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_4_4),
            Specialbefore(before=before_3_0_to_3_3_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_3_0_to_3_3_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_0_to_3_3_variation_4.
            Specialbefore(before=before_3_0_to_3_3_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_0_to_3_3_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_4_4),
            Specialbefore(before=before_3_0_to_3_3_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_3_0_to_3_3_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_1_to_3_4_variation_1.
            Specialbefore(before=before_3_1_to_3_4_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_1_to_3_4_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_1_to_3_4_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_3_1_to_3_4_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_1_to_3_4_variation_2.
            Specialbefore(before=before_3_1_to_3_4_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_1_to_3_4_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_1_to_3_4_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_3_1_to_3_4_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_1_to_3_4_variation_3.
            Specialbefore(before=before_3_1_to_3_4_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_1_to_3_4_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_1_to_3_4_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_3_1_to_3_4_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_1_to_3_4_variation_4.
            Specialbefore(before=before_3_1_to_3_4_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_1_to_3_4_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_1_to_3_4_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_5),
            Specialbefore(before=before_3_1_to_3_4_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_2_to_3_5_variation_1.
            Specialbefore(before=before_3_2_to_3_5_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_2_to_3_5_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_2_to_3_5_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_2_to_3_5_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_2_to_3_5_variation_2.
            Specialbefore(before=before_3_2_to_3_5_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_2_to_3_5_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_2_to_3_5_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_2_to_3_5_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_2_to_3_5_variation_3.
            Specialbefore(before=before_3_2_to_3_5_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_2_to_3_5_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_2_to_3_5_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_2_to_3_5_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_2_to_3_5_variation_4.
            Specialbefore(before=before_3_2_to_3_5_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_2_to_3_5_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_2_to_3_5_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_3_2_to_3_5_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_6),
            # All Specialbefores for before_3_3_to_3_6_variation_1.
            Specialbefore(before=before_3_3_to_3_6_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_3_to_3_6_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_3_to_3_6_variation_1,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_3_3_to_3_6_variation_2.
            Specialbefore(before=before_3_3_to_3_6_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_3_to_3_6_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_3_to_3_6_variation_2,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_3_3_to_3_6_variation_3.
            Specialbefore(before=before_3_3_to_3_6_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_3_to_3_6_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_3_to_3_6_variation_3,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_3_3_to_3_6_variation_4.
            Specialbefore(before=before_3_3_to_3_6_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_3_to_3_6_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_3_to_3_6_variation_4,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_3_3_to_3_6_variation_5.
            Specialbefore(before=before_3_3_to_3_6_variation_5,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_3_to_3_6_variation_5,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_3_to_3_6_variation_5,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_3_3_to_3_6_variation_6.
            Specialbefore(before=before_3_3_to_3_6_variation_6,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_3_to_3_6_variation_6,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_3_to_3_6_variation_6,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_3_3_to_3_6_variation_7.
            Specialbefore(before=before_3_3_to_3_6_variation_7,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_3_to_3_6_variation_7,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_3_to_3_6_variation_7,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_3_3_to_3_6_variation_8.
            Specialbefore(before=before_3_3_to_3_6_variation_8,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_3_3_to_3_6_variation_8,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_3_3_to_3_6_variation_8,
                          internal_directly_playable_square=directly_playable_square_3_3,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_4_3_to_4_6_variation_1.
            Specialbefore(before=before_4_3_to_4_6_variation_1,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_4_3_to_4_6_variation_1,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_4_3_to_4_6_variation_1,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_4_3_to_4_6_variation_1,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_3_3),
            # All Specialbefores for before_4_3_to_4_6_variation_2.
            Specialbefore(before=before_4_3_to_4_6_variation_2,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_4_3_to_4_6_variation_2,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_4_3_to_4_6_variation_2,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_4_3_to_4_6_variation_2,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_3_3),
            # All Specialbefores for before_4_3_to_4_6_variation_3.
            Specialbefore(before=before_4_3_to_4_6_variation_3,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_4_3_to_4_6_variation_3,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_4_3_to_4_6_variation_3,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_4_3_to_4_6_variation_3,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_3_3),
            # All Specialbefores for before_4_3_to_4_6_variation_4.
            Specialbefore(before=before_4_3_to_4_6_variation_4,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_4_3_to_4_6_variation_4,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_4_3_to_4_6_variation_4,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_0_2),
            Specialbefore(before=before_4_3_to_4_6_variation_4,
                          internal_directly_playable_square=directly_playable_square_4_4,
                          external_directly_playable_square=directly_playable_square_3_3),
            # All Specialbefores for before_2_3_to_5_6_variation_1.
            Specialbefore(before=before_2_3_to_5_6_variation_1,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_2_3_to_5_6_variation_1,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_2_3_to_5_6_variation_1,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_2_3_to_5_6_variation_2.
            Specialbefore(before=before_2_3_to_5_6_variation_2,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_2_3_to_5_6_variation_2,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_2_3_to_5_6_variation_2,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_2_3_to_5_6_variation_3.
            Specialbefore(before=before_2_3_to_5_6_variation_3,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_2_3_to_5_6_variation_3,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_2_3_to_5_6_variation_3,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_2_3_to_5_6_variation_4.
            Specialbefore(before=before_2_3_to_5_6_variation_4,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_2_3_to_5_6_variation_4,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_2_3_to_5_6_variation_4,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_2_3_to_5_6_variation_5.
            Specialbefore(before=before_2_3_to_5_6_variation_5,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_2_3_to_5_6_variation_5,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_2_3_to_5_6_variation_5,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_2_3_to_5_6_variation_6.
            Specialbefore(before=before_2_3_to_5_6_variation_6,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_2_3_to_5_6_variation_6,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_2_3_to_5_6_variation_6,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_2_3_to_5_6_variation_7.
            Specialbefore(before=before_2_3_to_5_6_variation_7,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_2_3_to_5_6_variation_7,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_2_3_to_5_6_variation_7,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_0_2),
            # All Specialbefores for before_2_3_to_5_6_variation_8.
            Specialbefore(before=before_2_3_to_5_6_variation_8,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_0),
            Specialbefore(before=before_2_3_to_5_6_variation_8,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_5_1),
            Specialbefore(before=before_2_3_to_5_6_variation_8,
                          internal_directly_playable_square=directly_playable_square_5_6,
                          external_directly_playable_square=directly_playable_square_0_2),
        }
        self.assertEqual(want_specialbefores, got_specialbefores)


if __name__ == '__main__':
    unittest.main()
