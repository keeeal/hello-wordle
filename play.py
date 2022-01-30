from functools import partial
from multiprocessing import Pool
from pathlib import Path
from random import shuffle

from game import Game
from players.entropy_player import EntropyPlayer as Player
from utils.input import read_files


def play_game(answer, allowed_guesses):
    game = Game([answer], allowed_guesses)
    player = Player(vocabulary=allowed_guesses)

    while not game.is_won:
        guess = player.guess()
        feedback = game.guess(guess)
        player.update(feedback)

    return game.n_guesses


if __name__ == "__main__":
    allowed_guesses, answers = read_files(
        Path("data") / "wordle-allowed-guesses.txt",
        Path("data") / "wordle-answers-alphabetical.txt",
    )

    shuffle(answers)

    with Pool() as p:
        game_lengths = p.map(
            partial(play_game, allowed_guesses=allowed_guesses), answers
        )

    print()
    print(sum(game_lengths) / len(game_lengths))
    print(max(game_lengths))
