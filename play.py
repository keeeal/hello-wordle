from pathlib import Path

from utils.data import load_words
from utils.game import Game, InvalidGuess
from utils.keyboard import Keyboard


def play():
    allowed = load_words(Path("data") / "wordle-allowed-guesses.txt")
    answers = load_words(Path("data") / "wordle-answers-alphabetical.txt")
    allowed.extend(answers)

    game = Game(answers, allowed)
    keyboard = Keyboard()

    while True:
        guess = input()

        try:
            feedback = game.guess(guess)
        except InvalidGuess:
            print(f"{guess} is not a valid word.")
        else:
            keyboard.update(guess, feedback)

            print(feedback)
            print(keyboard)

            if feedback.is_win():
                print("you win")
                return

            if len(game.guesses) >= 6:
                print("you lose")
                return


if __name__ == "__main__":
    play()
