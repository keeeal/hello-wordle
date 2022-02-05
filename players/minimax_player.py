

from functools import partial
from typing import Iterable, Optional, Sequence

from utils.word import is_valid
from game import Game


class MinimaxPlayer:
    def __init__(self, vocabulary: Sequence[str], first_guess: Optional[str] = None) -> None:
        self.vocabulary = list(vocabulary)
        self.valid_words = list(vocabulary)
        self.first_guess = first_guess
        self.last_guess: Optional[str] = None

    def guess(self) -> str:
        if self.first_guess and not self.last_guess:
            self.last_guess = self.first_guess
            return self.last_guess

        scores = {}

        for guess in self.vocabulary:
            words_remaining = []

            for answer in self.valid_words:
                feedback = Game([answer], [guess, answer]).guess(guess)
                words_remaining.append(sum(
                    is_valid(word, guess, feedback)
                    for word in self.valid_words
                ))

            scores[guess] = max(words_remaining)

        next_guesses = [guess for guess, score in scores.items() if score == min(scores.values())]
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
