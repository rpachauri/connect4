from abc import ABC, abstractmethod


class TranspositionTable(ABC):

    @abstractmethod
    def save(self, state, phi: int, delta: int):
        """Saves state with the given phi and delta numbers. Overwrites the phi/delta numbers if
        state is already saved in this TranspositionTable.

        Args:
            state (State): a state in the state space of a TwoPlayerGameEnv.
            phi (int): the phi number of the state to save.
            delta: the delta number of the state to save.
        """
        pass

    @abstractmethod
    def retrieve(self, state) -> (int, int):
        """
        Args:
            state (State): a state in the state space of a TwoPlayerGameEnv.

        Returns:
            phi (int): the phi number of the state to retrieve.
            delta: the delta number of the state to retrieve.
        """
        pass
