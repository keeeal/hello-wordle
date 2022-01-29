from random import choice, shuffle
from functools import partial
from string import ascii_lowercase
from math import log2

from input import read_files
from game import Game


def valid(word: str, last_guess, feedback) -> bool:
    for i, j, k in zip(word, last_guess, feedback):
        match k:
            case 0:
                if j in word:
                    return False
            case 1:
                if j not in word:
                    return False
                if i == j:
                    return False
            case 2:
                if i != j:
                    return False

    return True


class RandomPlayer:
    def __init__(self, words) -> None:
        self.words = words
        shuffle(self.words)
        self.iterator = iter(self.words)

    def guess(self) -> str:
        return next(self.iterator)

    def update(self, feedback):
        pass


class InvalidPlayer:
    def __init__(self, words) -> None:
        self.words = words
        self.last_guess = None

    def guess(self) -> str:
        self.last_guess = choice(self.words)
        return self.last_guess

    def update(self, feedback):
        self.words = list(
            filter(
                partial(valid, last_guess=self.last_guess, feedback=feedback),
                self.words,
            )
        )


class EntropyPlayer:
    def __init__(self, words) -> None:
        self.all_words = words
        self.words = words
        self.last_guess = None

    def guess(self) -> str:

        entropy = {}

        for letter in ascii_lowercase:
            data = [(letter in word) for word in self.words]
            p_true = sum(data) / len(data)
            p_false = 1 - p_true

            e = 0
            if p_true:
                e += p_true * log2(p_true)
            if p_false:
                e += p_false * log2(p_false)

            entropy[letter] = -e

        entropy_words = sorted(
            (sum(entropy[l] for l in set(w)), w) for w in self.words
        )

        # print()
        # print(entropy_words[-10:])
        # print()

        self.last_guess = entropy_words[-1][-1]

        return self.last_guess

    def update(self, feedback):
        self.words = list(
            filter(
                partial(valid, last_guess=self.last_guess, feedback=feedback),
                self.words,
            )
        )


if __name__ == "__main__":
    valid_words, answers = read_files(
        "wordle-allowed-guesses.txt", "wordle-answers-alphabetical.txt"
    )
    game_lengths = []

    for _ in range(1000):
        player = InvalidPlayer(valid_words)
        game = Game(answers, valid_words)

        while not game.is_won:
            guess = player.guess()
            # print(f"{guess=}")
            feedback = game.guess(guess)
            # print(f"{feedback=}")
            player.update(feedback)

        game_lengths.append(game.n_guesses)

    print()
    print(sum(game_lengths) / len(game_lengths))
    print(max(game_lengths))
