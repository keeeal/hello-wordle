from random import shuffle
from typing import Iterable, Sequence

class RandomPlayer:
    def __init__(self, vocabulary: Sequence[str]) -> None:
        self.vocabulary = list(vocabulary)
        shuffle(self.vocabulary)

    def guess(self) -> str:
        return self.vocabulary.pop()

    def update(self, feedback: Iterable[int]):
        pass
