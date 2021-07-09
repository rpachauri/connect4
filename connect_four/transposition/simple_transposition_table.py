from connect_four.transposition import TranspositionTable


class SimpleTranspositionTable(TranspositionTable):
    def __init__(self):
        self.transposition_to_phi_delta_numbers = {}

    def save(self, transposition: str, phi: int, delta: int):
        """Saves state with the given phi and delta numbers. Overwrites the phi/delta numbers if
        state is already saved in this TranspositionTable.

        Args:
            transposition (str): a transposition of a state in the state space of a TwoPlayerGameEnv.
            phi (int): the phi number of the state to save.
            delta: the delta number of the state to save.
        """
        self.transposition_to_phi_delta_numbers[transposition] = (phi, delta)

    def retrieve(self, transposition: str) -> (int, int):
        """
        Raises:
            KeyError: if state is not in this transposition table.

        Args:
            transposition (str): a transposition of a state in the state space of a TwoPlayerGameEnv.

        Returns:
            phi (int): the phi number of the state to retrieve.
            delta: the delta number of the state to retrieve.
        """
        return self.transposition_to_phi_delta_numbers[transposition]

    def __contains__(self, item):
        """

        Args:
            item (State): a transposition of a state in the state space of a TwoPlayerGameEnv.

        Returns:
            contained (bool): true if transposition is contained in this TranspositionTable; otherwise, false.
        """
        return item in self.transposition_to_phi_delta_numbers

    def close(self):
        pass
