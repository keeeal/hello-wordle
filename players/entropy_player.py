from functools import partial
from math import log2
from string import ascii_lowercase
from typing import Iterable, Optional, Sequence

from utils.word import is_valid


def safe_log2(x):
    try:
        return log2(x)
    except ValueError:
        return 0


class EntropyPlayer:
    def __init__(self, vocabulary: Sequence[str]) -> None:
        self.word_length = len(vocabulary[0])
        assert all(len(word) == self.word_length for word in vocabulary)

        self.vocabulary = list(vocabulary)
        self.valid_words = list(vocabulary)
        self.last_guess: Optional[str] = None

    def guess(self) -> str:

        entropy_per_letter = {}
        entropy_per_position = [{} for _ in range(self.word_length)]

        for letter in ascii_lowercase:
            p_true = sum((letter in word) for word in self.valid_words) / len(self.valid_words)
            entropy_per_letter[letter] = -sum(p * safe_log2(p) for p in (p_true, 1 - p_true))

        for n in range(self.word_length):
            for letter in ascii_lowercase:
                p_true = sum((letter == word[n]) for word in self.valid_words) / len(self.valid_words)
                entropy_per_position[n][letter] = -sum(p * safe_log2(p) for p in (p_true, 1 - p_true))

        def entropy(word: str) -> float:
            return sum(entropy_per_letter[letter] for letter in set(word)) \
                + sum(entropy_per_position[n][letter] for n, letter in enumerate(word))

        # this part is ad-hoc and there is probably a better way
        pool = self.valid_words if len(self.valid_words) < 3 else self.vocabulary

        self.last_guess = max(pool, key=entropy)
        self.vocabulary.remove(self.last_guess)
        return self.last_guess

    def update(self, feedback: Iterable[int]):
        self.valid_words = list(
            filter(
                partial(is_valid, last_guess=self.last_guess, feedback=feedback),
                self.valid_words,
            )
        )
