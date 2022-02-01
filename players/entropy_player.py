from functools import partial
from itertools import chain
from math import log2
from typing import Any, Iterable, Optional, Sequence

from utils.word import is_valid


def p_log_p(p: float) -> float:
    return p * log2(p) if p > 0 else 0


def binary_entropy(key: Any, seq: Sequence) -> float:
    p = seq.count(key) / len(seq)
    return -sum(map(p_log_p, (p, 1 - p)))


class EntropyPlayer:
    def __init__(self, vocabulary: Sequence[str]) -> None:
        self.vocabulary = list(vocabulary)
        self.valid_words = list(vocabulary)
        self.last_guess: Optional[str] = None

    def guess(self) -> str:
        words = self.valid_words if len(self.valid_words) <= 2 else self.vocabulary

        entropy_per_letter: dict[str, float] = {
            letter: binary_entropy(True, [letter in w for w in self.valid_words])
            for letter in set(chain(*words))
        }

        entropy_per_position: list[dict[str, float]] = [
            dict(zip(a, map(partial(binary_entropy, seq=b), a)))
            for a, b in zip(map(set, zip(*words)), zip(*self.valid_words))
        ]

        def entropy(word: str) -> float:
            return sum(entropy_per_letter[letter] for letter in set(word)) + \
                sum(entropy_per_position[n][letter] for n, letter in enumerate(word))

        self.last_guess = max(words, key=entropy)
        return self.last_guess

    def update(self, feedback: Iterable[int]):
        self.valid_words = list(
            filter(
                partial(is_valid, last_guess=self.last_guess, feedback=feedback),
                self.valid_words,
            )
        )
