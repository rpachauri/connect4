import unittest

import numpy as np

from connect_four.agents import FlatUCB

class TestFlatUCB(unittest.TestCase):
    def test_something(self):
        agent = FlatUCB()
        action_total_values = np.array([1, 10])
        action_visits = np.array([10, 1])
        action = agent._select_action_for_rollout(action_total_values, action_visits)
        self.assertEqual(1, action)


if __name__ == '__main__':
    unittest.main()
