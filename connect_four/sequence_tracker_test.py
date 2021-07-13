import unittest

from connect_four.sequence_tracker import SequenceTracker


class TestSequenceTracker(unittest.TestCase):
    def test_init(self):
        st = SequenceTracker(action_sequence=[3, 3, 3, 3, 3, 1, 1, 1])
        want_sequence = ["4", "4", "4", "4", "4", "2", "2", "2"]
        self.assertEqual(want_sequence, st.action_sequence)

    def test_move(self):
        st = SequenceTracker(action_sequence=[3, 3, 3, 3, 3, 1, 1, 1])
        st.move(action=2)
        want_sequence = ["4", "4", "4", "4", "4", "2", "2", "2", "3"]
        self.assertEqual(want_sequence, st.action_sequence)

    def test_serialize(self):
        st = SequenceTracker(action_sequence=[3, 3, 3, 3, 3, 1, 1, 1])
        want_serialization = "44444222"
        self.assertEqual(want_serialization, st.serialize())


if __name__ == '__main__':
    unittest.main()
