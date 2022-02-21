from random import choice
from typing import Sequence


class InvalidGuess(Exception):
    pass


class Feedback(tuple):
    def __new__(self, guess: str, answer: str):
        values = min(len(guess), len(answer)) * [0]
        guess_letters = list(guess)
        answer_letters = list(answer)

        for n, (i, j) in enumerate(zip(guess, answer)):
            if i == j:
                values[n] = 2
                guess_letters[n] = None
                answer_letters[n] = None

        for n, letter in enumerate(guess_letters):
            if letter and letter in answer_letters:
                values[n] = 1
                answer_letters.remove(letter)

        return super().__new__(Feedback, values)

    def __str__(self) -> str:
        return "".join(("⬜", "🟨", "🟩")[i] for i in self)

    def is_win(self) -> bool:
        return all(i == 2 for i in self)


class Game:
    def __init__(
        self,
        answers: Sequence[str],
        allowed: Sequence[str],
    ) -> None:
        self.answer = choice(answers)
        self.allowed = set(allowed)
        self.word_length = len(self.answer)

        for word in allowed:
            assert len(word) == self.word_length

        assert self.answer in self.allowed

        self.guesses = []
        self.feedback = []

    def guess(self, guess: str) -> Feedback:
        if guess not in self.allowed:
            raise InvalidGuess(guess)

        self.guesses.append(guess)
        feedback = Feedback(guess, self.answer)
        self.feedback.append(feedback)
        return feedback
