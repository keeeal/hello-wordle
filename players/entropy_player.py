from functools import partial
from itertools import chain
from math import log2
from multiprocessing import Pool
from typing import Iterable, Optional, Sequence

from utils.word import is_valid


def p_log_p(p: float) -> float:
    return p * log2(p) if p > 0 else 0


def entropy(x: Sequence[bool]) -> float:
    p = sum(x) / len(x)
    return -sum(map(p_log_p, (p, 1 - p)))


def score(word: str, letter_in_word: dict, letter_in_position: list[dict]):
    return sum(entropy(letter_in_word[letter]) for letter in word) + \
        sum(entropy(d[letter]) for d, letter in zip(letter_in_position, word))


class EntropyPlayer:
    def __init__(self, vocabulary: Sequence[str], first_guess: Optional[str] = None) -> None:
        self.vocabulary = list(vocabulary)
        self.valid_words = list(vocabulary)
        self.first_guess = first_guess
        self.last_guess: Optional[str] = None

    def guess(self) -> str:
        if self.first_guess and not self.last_guess:
            self.last_guess = self.first_guess
            return self.last_guess

        guesses = self.valid_words if len(self.valid_words) <= 2 else self.vocabulary

        letter_in_word: dict[str, list[bool]] = {
            letter: [letter in word for word in self.valid_words]
            for letter in set(chain(*guesses))
        }

        letter_in_position: list[dict[str, list[bool]]] = [
            {letter: [letter == i for i in b] for letter in a}
            for a, b in zip(map(set, zip(*guesses)), zip(*self.valid_words))
        ]

        with Pool() as p:
            scores = p.map(
                partial(
                    score,
                    letter_in_word=letter_in_word,
                    letter_in_position=letter_in_position,
                ),
                guesses,
            )

        self.last_guess = max(zip(scores, guesses))[1]
        return self.last_guess

    def update(self, feedback: Iterable[int]) -> None:
        self.valid_words = [
            word for word in self.valid_words
            if is_valid(word, self.last_guess, feedback)
        ]
