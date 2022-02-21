from functools import partial
from multiprocessing import Pool
from typing import Iterable, Optional

from utils.game import Feedback


def score(guess: str, answers: list[str]) -> float:
    words_remaining = []

    for answer in answers:
        # feedback = Game([answer], [answer, word]).guess(word)
        feedback = Feedback(guess, answer)
        words_remaining.append(
            sum(
                Feedback(guess, answer) == feedback
                for answer in answers
            )
        )

    return max(words_remaining)


class MinimaxPlayer:
    def __init__(
        self, vocabulary: dict[str, float], first_guess: Optional[str] = None
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
            if Feedback(self.last_guess, word) == feedback
        ]
