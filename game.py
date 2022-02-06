from itertools import chain
from pathlib import Path
from random import choice
from typing import Sequence

from utils.data import load_words
from utils.keyboard import Keyboard


class InvalidGuess(Exception):
    pass


class WrongLengthGuess(Exception):
    pass


class Feedback(tuple):
    def __str__(self) -> str:
        return "".join(("⬜", "🟨", "🟩")[i] for i in self)


class Game:
    def __init__(
        self,
        answers: Sequence[str],
        allowed_guesses: Sequence[str],
        word_length: int = 5,
    ) -> None:
        for word in chain(answers, allowed_guesses):
            assert len(word) == word_length

        for answer in answers:
            assert answer in allowed_guesses

        self.answer = choice(answers)
        self.allowed_guesses = allowed_guesses
        self.word_length = word_length
        self.is_won = False
        self.n_guesses = 0

    def guess(self, guess: str) -> Feedback:
        if len(guess) != self.word_length:
            raise WrongLengthGuess(guess)

        if guess not in self.allowed_guesses:
            raise InvalidGuess(guess)

        self.n_guesses += 1

        if guess == self.answer:
            self.is_won = True
            return Feedback(self.word_length * (2,))

        feedback = []

        for i, j in zip(guess, self.answer):
            if i == j:
                feedback.append(2)
            elif i in self.answer:
                feedback.append(1)
            else:
                feedback.append(0)

        return Feedback(feedback)


def play():
    allowed_guesses, answers = read_files(
        Path("data") / "wordle-allowed-guesses.txt",
        Path("data") / "wordle-answers-alphabetical.txt",
    )

    game = Game(answers, allowed_guesses)
    keyboard = Keyboard()

    while True:
        guess = input()

        try:
            feedback = game.guess(guess)
        except InvalidGuess:
            print(f"{guess} is not a valid word.")
        except WrongLengthGuess:
            print(f"Please enter a {game.word_length} letter word.")
        else:
            keyboard.update(guess, feedback)

            print(feedback)
            print(keyboard)

        if game.is_won:
            print("you win")
            return

        if game.n_guesses >= 6:
            print("you lose")
            return


if __name__ == "__main__":
    play()
