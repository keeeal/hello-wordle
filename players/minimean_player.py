from functools import partial
from multiprocessing import Pool
from typing import Iterable, Optional, Sequence

from utils.word import is_valid
from game import Game


def score(word: str, answers: list[str]) -> float:
    words_remaining = []

    for answer in answers:
        feedback = Game([answer], [answer, word]).guess(word)
        words_remaining.append(
            sum(is_valid(a, word, feedback) for a in answers)
        )

    return sum(words_remaining) / len(words_remaining)


class MinimeanPlayer:
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

        with Pool() as p:
            scores = p.map(partial(score, answers=self.valid_words), self.vocabulary)

        next_guesses = [
            guess for guess, score in zip(self.vocabulary, scores)
            if score == min(scores)
        ]
        self.last_guess = next_guesses[0]

        for next_guess in next_guesses:
            if next_guess in self.valid_words:
                self.last_guess = next_guess

        return self.last_guess

    def update(self, feedback: Iterable[int]) -> None:
        self.valid_words = [
            word for word in self.valid_words
            if is_valid(word, self.last_guess, feedback)
        ]
