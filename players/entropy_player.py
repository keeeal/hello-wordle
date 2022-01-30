
from functools import partial
from math import log2
from string import ascii_lowercase

from utils.word import is_valid

class EntropyPlayer:
    def __init__(self, vocabulary) -> None:
        self.valid_words = vocabulary
        self.last_guess = None

    def guess(self) -> str:
        entropy = {}

        for letter in ascii_lowercase:
            data = [(letter in word) for word in self.valid_words]
            p_true = sum(data) / len(data)
            p_false = 1 - p_true

            e = 0
            if p_true:
                e += p_true * log2(p_true)
            if p_false:
                e += p_false * log2(p_false)

            entropy[letter] = -e

        entropy_words = sorted(
            (sum(entropy[l] for l in set(w)), w) for w in self.valid_words
        )

        self.last_guess = entropy_words[-1][-1]
        return self.last_guess

    def update(self, feedback):
        self.valid_words = list(
            filter(
                partial(is_valid, last_guess=self.last_guess, feedback=feedback),
                self.valid_words,
            )
        )
