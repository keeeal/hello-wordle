
from code import interact
from random import choice
from itertools import chain
from typing import Iterable

from input import read_files

class Game:
    def __init__(self, answers: Iterable[str], valid_words: Iterable[str], word_length: int = 5) -> None:
        for word in chain(answers, valid_words):
            assert len(word) == word_length

        self.answer = choice(answers)
        self.valid_words = valid_words
        self.word_length = word_length

    def guess(self, guess: str) -> list[int]:
        if guess not in self.valid_words:
            return self.word_length * [-1]

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

    valid_words, answers = read_files("wordle-allowed-guesses.txt", "wordle-answers-alphabetical.txt")

    game = Game(answers, valid_words)

    feedback = [0, 0, 0, 0, 0]

    while not all((i == 2) for i in feedback):
        guess = input()
        feedback = game.guess(guess)
        print(feedback)

    print(choice(["impressive", "good job", "you win"]))

