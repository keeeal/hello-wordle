from itertools import chain
from pathlib import Path
from random import choice
from typing import Sequence

from utils.input import read_files
from utils.keyboard import Keyboard


class InvalidGuess(Exception):
    pass

class WrongLengthGuess(Exception):
    pass

class Game:
    def __init__(
        self,
        answers: Sequence[str],
        allowed_guesses: Sequence[str],
        word_length: int = 5,
    ) -> None:
        for word in chain(answers, allowed_guesses):
            assert len(word) == word_length

        self.answer = choice(answers)
        self.allowed_guesses = allowed_guesses
        self.word_length = word_length
        self.is_won = False
        self.n_guesses = 0

    def guess(self, guess: str) -> list[int]:
        if len(guess) != 5:
            raise WrongLengthGuess(guess)

        if guess not in self.allowed_guesses:
            raise InvalidGuess(guess)

        self.n_guesses += 1

        if guess == self.answer:
            self.is_won = True
            return self.word_length * [2]

        feedback = []

        for i, j in zip(guess, self.answer):
            if i == j:
                feedback.append(2)
            elif i in self.answer:
                feedback.append(1)
            else:
                feedback.append(0)

        return feedback


if __name__ == "__main__":
    allowed_guesses, answers = read_files(
        Path("data") / "wordle-allowed-guesses.txt",
        Path("data") / "wordle-answers-alphabetical.txt",
    )

    game = Game(answers, allowed_guesses)
    keyboard = Keyboard()

    while not game.is_won:
        guess = input()

        try:
            feedback = game.guess(guess)
        except InvalidGuess:
            print(f"{guess} is not a valid word.")
            continue
        except WrongLengthGuess:
            print("Please enter a 5 letter word.")
            continue

        print(feedback)
        print(*keyboard.board,sep="\n")
      

        if game.is_won:
            print("you win")
            break

        if game.n_guesses >= 6:
            print("you lose")
            break
