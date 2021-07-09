from connect_four.transposition import TranspositionTable


class SQLiteTranspositionTable(TranspositionTable):
    def __init__(self):
        pass

    def save(self, transposition: str, phi: int, delta: int):
        """Saves state with the given phi and delta numbers. Overwrites the phi/delta numbers if
        state is already saved in this TranspositionTable.

        Args:
            transposition (str): a transposition of a state in the state space of a TwoPlayerGameEnv.
            phi (int): the phi number of the state to save.
            delta: the delta number of the state to save.
        """
        pass

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
        pass

    def __contains__(self, item):
        """

        Args:
            item (State): a transposition of a state in the state space of a TwoPlayerGameEnv.

        Returns:
            contained (bool): true if transposition is contained in this TranspositionTable; otherwise, false.
        """
        pass
