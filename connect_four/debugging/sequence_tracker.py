from typing import List


class SequenceTracker:

    def __init__(self, action_sequence: List[int]):
        self.action_sequence = []
        for action in action_sequence:
            self.action_sequence.append(str(action + 1))

    def move(self, action: int):
        self.action_sequence.append(str(action + 1))

    def undo_move(self):
        self.action_sequence.pop()

    def serialize(self) -> str:
        return ''.join(self.action_sequence)
