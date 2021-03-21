from connect_four.transposition import TranspositionTable
from connect_four.transposition import hash_position


class TicTacToeSimpleTranspositionTable(TranspositionTable):
    def __init__(self):
        self.transposition_to_proof_disproof_numbers = {}

    def save(self, state, proof: int, disproof: int):
        """Saves state with the given proof and disproof numbers. Overwrites the proof/disproof numbers if
        state is already saved in this TranspositionTable.

        Args:
            state (State): a state in the state space of a TwoPlayerGameEnv.
            proof (int): the proof number of the state to save.
            disproof: the disproof number of the state to save.
        """
        transposition = hash_position(state=state)
        self.transposition_to_proof_disproof_numbers[transposition] = (proof, disproof)

    def retrieve(self, state) -> (int, int):
        """
        Raises:
            KeyError: if state is not in this transposition table.

        Args:
            state (State): a state in the state space of a TwoPlayerGameEnv.

        Returns:
            proof (int): the proof number of the state to retrieve.
            disproof: the disproof number of the state to retrieve.
        """
        transposition = hash_position(state=state)
        return self.transposition_to_proof_disproof_numbers[transposition]
