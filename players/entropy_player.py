from functools import partial
from math import log, log2, exp
from multiprocessing import Pool
from typing import Iterable, Optional

from utils.game import Feedback


def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))


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


def normalise_frequencies(
    vocabulary: dict[str, float], scale: float
) -> dict[str, float]:
    words, freqs = zip(*vocabulary.items())
    inv_freqs = [1 - f for f in freqs]
    alpha = 1 + len(inv_freqs) / sum(map(log, inv_freqs))
    lin_inv_freqs = [pow(f, -alpha) for f in inv_freqs]
    lin_freqs = [1 - f for f in lin_inv_freqs]
    mean_lin_freq = sum(lin_freqs) / len(lin_freqs)
    lin_freqs = [scale * (f - mean_lin_freq) for f in lin_freqs]
    return dict(zip(words, map(sigmoid, lin_freqs)))


class EntropyPlayer:
    def __init__(
        self, vocabulary: dict[str, float], first_guess: Optional[str] = None
    ) -> None:
        self.vocabulary = list(vocabulary)
        self.valid_words = list(vocabulary)
        self.frequencies = normalise_frequencies(vocabulary, scale=10)
        self.first_guess = first_guess
        self.last_guess = None

    def guess(self) -> str:
        if self.first_guess and not self.last_guess:
            self.last_guess = self.first_guess
            return self.last_guess

        guesses = self.valid_words if len(self.valid_words) <= 2 else self.vocabulary
        valid_freqs = {word: self.frequencies[word] for word in self.valid_words}

        with Pool() as p:
            scores = p.map(partial(entropy, answers=valid_freqs), guesses)

        self.last_guess = max(zip(scores, guesses))[1]
        return self.last_guess

    def update(self, feedback: Iterable[int]) -> None:
        self.valid_words = [
            word for word in self.valid_words
            if Feedback(self.last_guess, word) == feedback
        ]
