from connect_four.transposition import TranspositionTable
from connect_four.transposition import hash_position


class TicTacToeSimpleTranspositionTable(TranspositionTable):
    def __init__(self):
        self.transposition_to_phi_delta_numbers = {}

    def save(self, state, phi: int, delta: int):
        """Saves state with the given phi and delta numbers. Overwrites the phi/delta numbers if
        state is already saved in this TranspositionTable.

        Args:
            state (State): a state in the state space of a TwoPlayerGameEnv.
            phi (int): the phi number of the state to save.
            delta: the delta number of the state to save.
        """
        transposition = hash_position(state=state)
        self.transposition_to_phi_delta_numbers[transposition] = (phi, delta)

    def retrieve(self, state) -> (int, int):
        """
        Raises:
            KeyError: if state is not in this transposition table.

        Args:
            state (State): a state in the state space of a TwoPlayerGameEnv.

        Returns:
            phi (int): the phi number of the state to retrieve.
            delta: the delta number of the state to retrieve.
        """
        transposition = hash_position(state=state)
        return self.transposition_to_phi_delta_numbers[transposition]
