
from functools import partial
from random import choice

from utils.word import is_valid

class ValidPlayer:
    def __init__(self, vocabulary) -> None:
        self.valid_words = vocabulary
        self.last_guess = None

    def guess(self) -> str:
        self.last_guess = choice(self.valid_words)
        return self.last_guess

    def update(self, feedback):
        self.valid_words = list(
            filter(
                partial(is_valid, last_guess=self.last_guess, feedback=feedback),
                self.valid_words,
            )
        )
