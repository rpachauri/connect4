from collections import namedtuple
from enum import Enum


Square = namedtuple("Square", ["row", "col"])
Group = namedtuple("Group", ["squares"])


class SquareType(Enum):
    Empty = 0
    Indifferent = 1
    Player1 = 2
    Player2 = 3
