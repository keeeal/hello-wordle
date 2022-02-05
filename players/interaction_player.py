from itertools import chain, combinations, product
from math import log2
from typing import Iterable, Optional, Sequence

from utils.word import is_valid


def p_log_p(p: float) -> float:
    return p * log2(p) if p > 0 else 0


def joint_entropy(*x: Sequence[bool]) -> float:
    p = (
        sum(i == j for i in zip(*x)) / min(map(len, x))
        for j in product(*len(x) * [(True, False)])
    )
    return -sum(map(p_log_p, p))


def interaction_information(*x: Sequence[bool]) -> float:
    return sum(
        pow(-1, len(t) - 1) * joint_entropy(*t)
        for t in chain(*(combinations(x, r + 1) for r in range(len(x))))
    )


class InteractionPlayer:
    def __init__(
        self, vocabulary: Sequence[str], first_guess: Optional[str] = None
    ) -> None:
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

        def score(word: str) -> float:
            return interaction_information(
                *map(letter_in_word.get, word),
                *(d[letter] for d, letter in zip(letter_in_position, word))
            )

        self.last_guess = max(guesses, key=score)
        return self.last_guess

    def update(self, feedback: Iterable[int]) -> None:
        self.valid_words = [
            word for word in self.valid_words
            if is_valid(word, self.last_guess, feedback)
        ]
