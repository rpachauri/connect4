from connect_four.transposition import TranspositionTable


class TicTacToeSimpleTranspositionTable(TranspositionTable):

    def save(self, state, proof: int, disproof: int):
        pass

    def retrieve(self, state) -> (int, int):
        pass
