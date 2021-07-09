import sqlite3

from connect_four.transposition import TranspositionTable


class SQLiteTranspositionTable(TranspositionTable):
    def __init__(self, database_file: str):
        self.con = sqlite3.connect(database=database_file)
        self.cursor = self.con.cursor()
        create_phi_delta_table_sql = """CREATE TABLE IF NOT EXISTS
        PhiDelta(
            Transposition TEXT PRIMARY KEY,
            Phi INTEGER,
            Delta INTEGER
        )"""
        self.cursor.execute(create_phi_delta_table_sql)

    def save(self, transposition: str, phi: int, delta: int):
        """Saves state with the given phi and delta numbers. Overwrites the phi/delta numbers if
        state is already saved in this TranspositionTable.

        Args:
            transposition (str): a transposition of a state in the state space of a TwoPlayerGameEnv.
            phi (int): the phi number of the state to save.
            delta: the delta number of the state to save.
        """
        if not self.__contains__(item=transposition):
            insert_sql = """INSERT INTO PhiDelta(Transposition, Phi, Delta) VALUES(?, ?, ?)"""
            self.cursor.execute(insert_sql, (transposition, phi, delta))
        else:
            update_sql = """UPDATE PhiDelta SET Phi = ?, Delta = ? WHERE Transposition = ?"""
            self.cursor.execute(update_sql, (phi, delta, transposition))

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
        read_sql = """SELECT Phi, Delta FROM PhiDelta WHERE Transposition=?"""
        self.cursor.execute(read_sql, [transposition])
        return self.cursor.fetchone()

    def __contains__(self, item):
        """

        Args:
            item (State): a transposition of a state in the state space of a TwoPlayerGameEnv.

        Returns:
            contained (bool): true if transposition is contained in this TranspositionTable; otherwise, false.
        """
        read_sql = """SELECT 1 FROM PhiDelta WHERE Transposition=?"""
        self.cursor.execute(read_sql, [item])
        return self.cursor.fetchone() is not None

    def close(self):
        self.cursor.close()
        self.con.close()
