from random import choice
from typing import Iterable, Optional, Sequence

from utils.word import is_valid

class ValidPlayer:
    def __init__(self, vocabulary: Sequence[str], first_guess: Optional[str] = None) -> None:
        self.valid_words = list(vocabulary)
        self.first_guess = first_guess
        self.last_guess: Optional[str] = None

    def guess(self) -> str:
        if self.first_guess and not self.last_guess:
            self.last_guess = self.first_guess
        else:
            self.last_guess = choice(self.valid_words)
        return self.last_guess

    def update(self, feedback: Iterable[int]) -> None:
        self.valid_words = [
            word for word in self.valid_words
            if is_valid(word, self.last_guess, feedback)
        ]
