import dbm

from connect_four.transposition import TranspositionTable


class DBMTranspositionTable(TranspositionTable):
    def __init__(self, phi_file: str, delta_file: str):
        self.phi_db = dbm.open(phi_file, "c")
        self.delta_db = dbm.open(delta_file, "c")

    def save(self, transposition: str, phi: int, delta: int):
        """Saves state with the given phi and delta numbers. Overwrites the phi/delta numbers if
        state is already saved in this TranspositionTable.

        Args:
            transposition (str): a transposition of a state in the state space of a TwoPlayerGameEnv.
            phi (int): the phi number of the state to save.
            delta: the delta number of the state to save.
        """
        phi_bytes = phi.to_bytes(length=8, byteorder="big", signed=False)
        self.phi_db[transposition] = phi_bytes
        delta_bytes = delta.to_bytes(length=8, byteorder="big", signed=False)
        self.delta_db[transposition] = delta_bytes

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
        phi = int.from_bytes(bytes=self.phi_db[transposition], byteorder="big", signed=False)
        delta = int.from_bytes(bytes=self.delta_db[transposition], byteorder="big", signed=False)
        return phi, delta

    def __contains__(self, item):
        """

        Args:
            item (State): a transposition of a state in the state space of a TwoPlayerGameEnv.

        Returns:
            contained (bool): true if transposition is contained in this TranspositionTable; otherwise, false.
        """
        return item in self.phi_db and item in self.delta_db

    def close(self):
        self.phi_db.close()
        self.delta_db.close()
