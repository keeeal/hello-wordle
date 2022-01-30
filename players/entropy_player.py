from functools import partial
from math import log2
from string import ascii_lowercase

from utils.word import is_valid


def safe_log2(x):
    try:
        return log2(x)
    except ValueError:
        return 0


class EntropyPlayer:
    def __init__(self, vocabulary) -> None:
        self.valid_words = vocabulary
        self.last_guess = None

    def guess(self) -> str:
        entropy_per_letter = {}
        entropy_per_position = [{} for _ in range(5)]
        entropy_per_word = {}

        for letter in ascii_lowercase:
            p_true = sum((letter in word) for word in self.valid_words) / len(self.valid_words)
            entropy_per_letter[letter] = -sum(p * safe_log2(p) for p in (p_true, 1 - p_true))

        for position in range(5):
            for letter in ascii_lowercase:
                p_true = sum((letter == word[position]) for word in self.valid_words) / len(self.valid_words)
                entropy_per_position[position][letter] = -sum(p * safe_log2(p) for p in (p_true, 1 - p_true))

        for word in self.valid_words:
            entropy_per_word[word] = sum(
                entropy_per_letter[letter] for letter in set(word)
            ) + sum(
                entropy_per_position[position][word[position]] for position in range(5)
            )

        self.last_guess = max(self.valid_words, key=entropy_per_word.get)
        return self.last_guess

    def update(self, feedback):
        self.valid_words = list(
            filter(
                partial(is_valid, last_guess=self.last_guess, feedback=feedback),
                self.valid_words,
            )
        )
