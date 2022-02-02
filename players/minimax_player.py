

from functools import partial
from random import choices
from typing import Iterable, Optional, Sequence

from utils.word import is_valid
from game import Game


class MinimaxPlayer:
    def __init__(self, vocabulary: Sequence[str]) -> None:
        self.vocabulary = list(vocabulary)
        self.valid_words = list(vocabulary)  # S
        self.last_guess: Optional[str] = None

    def guess(self) -> str:

        word_scores = {}

        for word in self.vocabulary:
            words_remaining = []

            for valid_word in choices(self.valid_words, k=100):
                feedback = Game([valid_word], [word]).guess(word)
                remaining_words = sum(
                    map(
                        partial(is_valid, last_guess=word, feedback=feedback),
                        self.valid_words
                    )
                )

                words_remaining.append(remaining_words)

            word_scores[word] = max(words_remaining)

        next_guesses = [word for word, score in word_scores.items() if score == min(word_scores.values())]
        self.last_guess = next_guesses[0]

        for next_guess in next_guesses:
            if next_guess in self.valid_words:
                self.last_guess = next_guess

        return self.last_guess

    def update(self, feedback: Iterable[int]):
        self.valid_words = list(
            filter(
                partial(is_valid, last_guess=self.last_guess, feedback=feedback),
                self.valid_words,
            )
        )
