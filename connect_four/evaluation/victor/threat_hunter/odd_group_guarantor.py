from abc import ABC, abstractmethod
from typing import Set


class OddGroupGuarantor(ABC):

    @abstractmethod
    def columns(self) -> Set[int]:
        pass
