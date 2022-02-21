from functools import partial
from math import log2
from multiprocessing import Pool
from typing import Iterable, Optional

from utils.game import Feedback


def p_log_p(p: float) -> float:
    return p * log2(p) if p > 0 else 0


def entropy(guess: str, answers: dict[str, float]) -> float:
    feedback: dict[Feedback, list[str]] = dict()

    for answer in answers:
        f = Feedback(guess, answer)
        feedback[f] = feedback.get(f, []) + [answer]

    total = sum(answers.values())
    p = [sum(map(answers.get, feedback[f])) / total for f in feedback]
    return -sum(map(p_log_p, p))


class EntropyPlayer:
    def __init__(
        self, vocabulary: dict[str, float], first_guess: Optional[str] = None
    ) -> None:
        self.vocabulary = vocabulary
        self.valid_words = list(vocabulary)
        self.first_guess = first_guess
        self.last_guess = None

    def guess(self) -> str:
        if self.first_guess and not self.last_guess:
            self.last_guess = self.first_guess
            return self.last_guess

        guesses = self.valid_words if len(self.valid_words) <= 2 else list(self.vocabulary)
        valid_freqs = {word: self.vocabulary[word] for word in self.valid_words}

        with Pool() as p:
            scores = p.map(partial(entropy, answers=valid_freqs), guesses)

        self.last_guess = max(zip(scores, guesses))[1]
        return self.last_guess

    def update(self, feedback: Iterable[int]) -> None:
        self.valid_words = [
            word for word in self.valid_words
            if Feedback(self.last_guess, word) == feedback
        ]
