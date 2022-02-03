from random import shuffle
from typing import Iterable, Optional, Sequence

class RandomPlayer:
    def __init__(self, vocabulary: Sequence[str], first_guess: Optional[str] = None) -> None:
        self.vocabulary = list(vocabulary)
        shuffle(self.vocabulary)
        if first_guess:
            self.vocabulary.insert(0, first_guess)

    def guess(self) -> str:
        return self.vocabulary.pop()

    def update(self, feedback: Iterable[int]) -> None:
        pass
