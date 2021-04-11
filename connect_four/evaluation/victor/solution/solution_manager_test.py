import unittest

import gym
import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.evaluation.victor.rules import Claimeven, Baseinverse, Vertical, Aftereven, Lowinverse, Highinverse, \
    Baseclaim, Before, Specialbefore
from connect_four.evaluation.victor.solution import solution2
from connect_four.evaluation.victor.solution.solution_manager import SolutionManager
from connect_four.game import Square
from connect_four.problem import Group


class TestSolutionManager(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_initialization_diagram_7_2(self):
        # This test case is based on Diagram 5.4 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 1, 1, ],
                [0, 0, 1, 1, 0, 1, 0, ],
                [0, 0, 0, 0, 1, 1, 1, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 1, 0, ],
            ],
            [
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 1, 1, ],
                [0, 0, 0, 0, 1, 1, 0, ],
                [0, 1, 1, 0, 0, 0, 1, ],
            ],
        ])
        sm = SolutionManager(env_variables=self.env.env_variables)

        # Rule instances that will be used to form Solutions.
        # Claimeven instances.
        claimeven_a1_a2 = Claimeven(
            upper=Square(row=4, col=0),  # a2
            lower=Square(row=5, col=0),  # a1
        )
        claimeven_a3_a4 = Claimeven(
            upper=Square(row=2, col=0),  # a4
            lower=Square(row=3, col=0),  # a3
        )
        # Vertical instances.
        vertical_a4_a5 = Vertical(
            upper=Square(row=1, col=0),  # a5
            lower=Square(row=2, col=0),  # a4
        )
        vertical_a2_a3 = Vertical(
            upper=Square(row=3, col=0),  # a3
            lower=Square(row=4, col=0),  # a2
        )
        vertical_b4_b5 = Vertical(
            upper=Square(row=1, col=1),  # b5
            lower=Square(row=2, col=1),  # b4
        )
        # Lowinverse instances.
        lowinverse_a4_a5_b4_b5 = Lowinverse(
            first_vertical=vertical_a4_a5,
            second_vertical=vertical_b4_b5,
        )
        lowinverse_a2_a3_b4_b5 = Lowinverse(
            first_vertical=vertical_a2_a3,
            second_vertical=vertical_b4_b5,
        )
        # Before instances.
        vertical_a3_a4 = Vertical(
            upper=Square(row=2, col=0),  # a4
            lower=Square(row=3, col=0),  # a3
        )
        before_a2_d2 = Before(
            group=Group(player=0, start=Square(row=4, col=0), end=Square(row=4, col=3)),  # a2-d2
            verticals=[vertical_a2_a3],
            claimevens=[],
        )
        before_a3_d3_variation_1 = Before(
            group=Group(player=1, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
            verticals=[vertical_a2_a3],
            claimevens=[],
        )
        before_a3_d3_variation_2 = Before(
            group=Group(player=1, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
            verticals=[vertical_a3_a4],
            claimevens=[],
        )
        before_a4_d4_variation_1 = Before(
            group=Group(player=1, start=Square(row=2, col=0), end=Square(row=2, col=3)),  # a4-d4
            verticals=[vertical_b4_b5],
            claimevens=[claimeven_a3_a4],
        )
        before_a4_d4_variation_2 = Before(
            group=Group(player=1, start=Square(row=2, col=0), end=Square(row=2, col=3)),  # a4-d4
            verticals=[vertical_a4_a5, vertical_b4_b5],
            claimevens=[],
        )
        before_a5_d5_variation_1 = Before(
            group=Group(player=0, start=Square(row=1, col=0), end=Square(row=1, col=3)),  # a5-d5
            verticals=[vertical_a4_a5, vertical_b4_b5],
            claimevens=[],
        )
        vertical_b5_b6 = Vertical(
            upper=Square(row=0, col=1),  # b6
            lower=Square(row=1, col=1),  # b5
        )
        before_a5_d5_variation_2 = Before(
            group=Group(player=0, start=Square(row=1, col=0), end=Square(row=1, col=3)),  # a5-d5
            verticals=[vertical_a4_a5, vertical_b5_b6],
            claimevens=[],
        )
        vertical_a5_a6 = Vertical(
            upper=Square(row=0, col=0),  # a6
            lower=Square(row=1, col=0),  # a5
        )
        before_a5_d5_variation_3 = Before(
            group=Group(player=0, start=Square(row=1, col=0), end=Square(row=1, col=3)),  # a5-d5
            verticals=[vertical_a5_a6, vertical_b4_b5],
            claimevens=[],
        )
        before_a5_d5_variation_4 = Before(
            group=Group(player=0, start=Square(row=1, col=0), end=Square(row=1, col=3)),  # a5-d5
            verticals=[vertical_a5_a6, vertical_b5_b6],
            claimevens=[],
        )
        before_b5_e2_variation_1 = Before(
            group=Group(player=1, start=Square(row=1, col=1), end=Square(row=4, col=4)),  # b5-e2
            verticals=[vertical_b4_b5],
            claimevens=[],
        )
        before_b5_e2_variation_2 = Before(
            group=Group(player=1, start=Square(row=1, col=1), end=Square(row=4, col=4)),  # b5-e2
            verticals=[vertical_b5_b6],
            claimevens=[],
        )

        want_solutions = {
            # Claimeven Solutions.
            solution2.from_claimeven(claimeven=Claimeven(
                upper=Square(row=0, col=0),  # a6
                lower=Square(row=1, col=0),  # a5
            )),
            solution2.from_claimeven(claimeven=claimeven_a3_a4),
            solution2.from_claimeven(claimeven=claimeven_a1_a2),
            solution2.from_claimeven(claimeven=Claimeven(
                upper=Square(row=0, col=1),  # b6
                lower=Square(row=1, col=1),  # b5
            )),
            # Baseinverse Solutions.
            solution2.from_baseinverse(baseinverse=Baseinverse(
                playable1=Square(row=5, col=0),  # a1
                playable2=Square(row=2, col=1),  # b4
            )),
            solution2.from_baseinverse(baseinverse=Baseinverse(
                playable1=Square(row=5, col=0),  # a1
                playable2=Square(row=0, col=4),  # e6
            )),
            solution2.from_baseinverse(baseinverse=Baseinverse(
                playable1=Square(row=2, col=1),  # b4
                playable2=Square(row=0, col=4),  # e6
            )),
            # Vertical Solutions.
            solution2.from_vertical(vertical=vertical_a4_a5),
            solution2.from_vertical(vertical=vertical_a2_a3),
            solution2.from_vertical(vertical=vertical_b4_b5),
            # Aftereven Solutions.
            solution2.from_aftereven(aftereven=Aftereven(
                group=Group(player=0, start=Square(row=4, col=0), end=Square(row=4, col=3)),  # a2-d2
                claimevens=[claimeven_a1_a2],
            )),
            # Lowinverse Solutions.
            solution2.from_lowinverse(lowinverse=lowinverse_a4_a5_b4_b5),
            solution2.from_lowinverse(lowinverse=lowinverse_a2_a3_b4_b5),
            # Highinverse Solutions.
            solution2.from_highinverse(highinverse=Highinverse(
                lowinverse=lowinverse_a4_a5_b4_b5,
                directly_playable_squares=[Square(row=2, col=1)],  # b4
            )),
            solution2.from_highinverse(highinverse=Highinverse(
                lowinverse=lowinverse_a2_a3_b4_b5,
                directly_playable_squares=[Square(row=2, col=1)],  # b4
            )),
            # Baseclaim Solutions.
            solution2.from_baseclaim(baseclaim=Baseclaim(
                first=Square(row=0, col=4),  # e6
                second=Square(row=5, col=0),  # a1
                third=Square(row=2, col=1),  # b4
            )),
            # Before Solutions.
            solution2.from_before(before=before_a2_d2),
            solution2.from_before(before=before_a3_d3_variation_1),
            solution2.from_before(before=before_a3_d3_variation_2),
            solution2.from_before(before=before_a4_d4_variation_1),
            solution2.from_before(before=before_a4_d4_variation_2),
            solution2.from_before(before=before_a5_d5_variation_1),
            solution2.from_before(before=before_a5_d5_variation_2),
            solution2.from_before(before=before_a5_d5_variation_3),
            solution2.from_before(before=before_a5_d5_variation_4),
            solution2.from_before(before=before_b5_e2_variation_1),
            solution2.from_before(before=before_b5_e2_variation_2),
            # Specialbefore Solutions.
            # Note that a1 cannot be used with a4-d4 Befores because it is in the same
            # column as one of the empty squares of the Before.
            solution2.from_specialbefore(specialbefore=Specialbefore(
                before=before_a4_d4_variation_1,
                internal_directly_playable_square=Square(row=2, col=1),  # b4
                external_directly_playable_square=Square(row=0, col=4),  # e6
            )),
            solution2.from_specialbefore(specialbefore=Specialbefore(
                before=before_a4_d4_variation_2,
                internal_directly_playable_square=Square(row=2, col=1),  # b4
                external_directly_playable_square=Square(row=0, col=4),  # e6
            )),
            # OddThreat Solutions.
            # None.
        }
        self.assertEqual(want_solutions, sm.solutions_by_move[0])

    def test_move_a1_from_diagram_7_2(self):
        # This test case is based on Diagram 5.4 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 1, 1, ],
                [0, 0, 1, 1, 0, 1, 0, ],
                [0, 0, 0, 0, 1, 1, 1, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 1, 0, ],
            ],
            [
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 1, 1, ],
                [0, 0, 0, 0, 1, 1, 0, ],
                [0, 1, 1, 0, 0, 0, 1, ],
            ],
        ])
        sm = SolutionManager(env_variables=self.env.env_variables)

        # Rule instances that will be used to form Solutions.
        # Claimeven instances.
        claimeven_a1_a2 = Claimeven(
            upper=Square(row=4, col=0),  # a2
            lower=Square(row=5, col=0),  # a1
        )
        # Vertical instances.
        vertical_a2_a3 = Vertical(
            upper=Square(row=3, col=0),  # a3
            lower=Square(row=4, col=0),  # a2
        )
        vertical_b4_b5 = Vertical(
            upper=Square(row=1, col=1),  # b5
            lower=Square(row=2, col=1),  # b4
        )
        # Lowinverse instances.
        lowinverse_a2_a3_b4_b5 = Lowinverse(
            first_vertical=vertical_a2_a3,
            second_vertical=vertical_b4_b5,
        )
        # Before instances.
        before_a2_d2 = Before(
            group=Group(player=0, start=Square(row=4, col=0), end=Square(row=4, col=3)),  # a2-d2
            verticals=[vertical_a2_a3],
            claimevens=[],
        )

        want_removed_solutions = {
            # Claimeven Solutions.
            solution2.from_claimeven(claimeven=claimeven_a1_a2),
            # Baseinverse Solutions.
            solution2.from_baseinverse(baseinverse=Baseinverse(
                playable1=Square(row=5, col=0),  # a1
                playable2=Square(row=2, col=1),  # b4
            )),
            solution2.from_baseinverse(baseinverse=Baseinverse(
                playable1=Square(row=5, col=0),  # a1
                playable2=Square(row=0, col=4),  # e6
            )),
            # Vertical Solutions.
            # None.
            # Aftereven Solutions.
            solution2.from_aftereven(aftereven=Aftereven(
                group=Group(player=0, start=Square(row=4, col=0), end=Square(row=4, col=3)),  # a2-d2
                claimevens=[claimeven_a1_a2],
            )),
            # Lowinverse Solutions.
            # None.
            # Highinverse Solutions.
            solution2.from_highinverse(highinverse=Highinverse(
                lowinverse=lowinverse_a2_a3_b4_b5,
                # a2 is now directly playable, causing this Highinverse to be stale.
                directly_playable_squares=[Square(row=2, col=1)],  # b4
            )),
            # Baseclaim Solutions.
            solution2.from_baseclaim(baseclaim=Baseclaim(
                first=Square(row=0, col=4),  # e6
                second=Square(row=5, col=0),  # a1
                third=Square(row=2, col=1),  # b4
            )),
            # Before Solutions.
            # None.
            # Specialbefore Solutions.
            # None.
            # OddThreat Solutions.
            # None.
        }
        want_added_solutions = {
            # Claimeven Solutions.
            # None.
            # Baseinverse Solutions.
            solution2.from_baseinverse(baseinverse=Baseinverse(
                playable1=Square(row=4, col=0),  # a2
                playable2=Square(row=2, col=1),  # b4
            )),
            solution2.from_baseinverse(baseinverse=Baseinverse(
                playable1=Square(row=4, col=0),  # a2
                playable2=Square(row=0, col=4),  # e6
            )),
            # Vertical Solutions.
            # None.
            # Aftereven Solutions.
            # None.
            # Lowinverse Solutions.
            # None.
            # Highinverse Solutions.
            solution2.from_highinverse(highinverse=Highinverse(
                lowinverse=lowinverse_a2_a3_b4_b5,
                # a2 is now directly playable, causing this Highinverse to be stale.
                directly_playable_squares=[
                    Square(row=4, col=0),  # a2
                    Square(row=2, col=1),  # b4
                ],
            )),
            # Baseclaim Solutions.
            # None.
            # Before Solutions.
            # None.
            # Specialbefore Solutions.
            solution2.from_specialbefore(specialbefore=Specialbefore(
                before=before_a2_d2,
                internal_directly_playable_square=Square(row=4, col=0),  # a2
                external_directly_playable_square=Square(row=2, col=1),  # b4
            )),
            solution2.from_specialbefore(specialbefore=Specialbefore(
                before=before_a2_d2,
                internal_directly_playable_square=Square(row=4, col=0),  # a2
                external_directly_playable_square=Square(row=0, col=4),  # e6
            )),
            # OddThreat Solutions.
            # None.
        }
        got_removed_solutions, got_added_solutions = sm.move(player=0, row=5, col=0)
        self.assertEqual(want_removed_solutions, got_removed_solutions)
        self.assertEqual(want_added_solutions, got_added_solutions)

    def test_undo_move_raises_assertion_error(self):
        # undo_move() should raise an assertion error if the SM is at the given state.
        sm = SolutionManager(env_variables=self.env.env_variables)
        with self.assertRaises(AssertionError):
            sm.undo_move()

    def test_move_undo_move(self):
        # Initialize variables.
        player, row, col = 0, 5, 0
        sm = SolutionManager(env_variables=self.env.env_variables)

        # Validate internal variables upon initialization.
        self.assertEqual(0, sm.board.state[player][row][col])
        self.assertFalse(sm.moves)

        # Validate internal variables after moving.
        sm.move(player=player, row=row, col=col)
        self.assertEqual(1, sm.board.state[player][row][col])
        self.assertEqual((player, row, col), sm.moves[0])

        # Validate internal variables equal to what they were upon initialization.
        sm.undo_move()
        self.assertEqual(0, sm.board.state[player][row][col])
        self.assertFalse(sm.moves)


if __name__ == '__main__':
    unittest.main()
