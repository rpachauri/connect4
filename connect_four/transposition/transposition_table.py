from abc import ABC, abstractmethod


class TranspositionTable(ABC):

    @abstractmethod
    def save(self, state, proof: int, disproof: int):
        """Saves state with the given proof and disproof numbers. Overwrites the proof/disproof numbers if
        state is already saved in this TranspositionTable.

        Args:
            state (State): a state in the state space of a TwoPlayerGameEnv.
            proof (int): the proof number of the state to save.
            disproof: the disproof number of the state to save.
        """
        pass

    @abstractmethod
    def retrieve(self, state) -> (int, int):
        """
        Args:
            state (State): a state in the state space of a TwoPlayerGameEnv.

        Returns:
            proof (int): the proof number of the state to retrieve.
            disproof: the disproof number of the state to retrieve.
        """
        pass
