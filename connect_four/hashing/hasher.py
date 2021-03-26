from abc import ABC, abstractmethod


# noinspection SpellCheckingInspection
class Hasher(ABC):

    @abstractmethod
    def move(self, action: int):
        pass

    @abstractmethod
    def undo_move(self):
        pass

    @abstractmethod
    def hash(self) -> str:
        pass
