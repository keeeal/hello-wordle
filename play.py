from email.policy import default
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from random import shuffle

from game import Game
from utils.input import read_files

from players.random_player import RandomPlayer
from players.valid_player import ValidPlayer
from players.entropy_player import EntropyPlayer


def play_game(answer, player, allowed_guesses):
    game = Game([answer], allowed_guesses)
    player = player(vocabulary=allowed_guesses)

    while not game.is_won:
        guess = player.guess()
        feedback = game.guess(guess)
        player.update(feedback)

    return game.n_guesses


def main(player):
    match player:
        case "random":
            Player = RandomPlayer
        case "valid":
            Player = ValidPlayer
        case "entropy":
            Player = EntropyPlayer

    allowed_guesses, answers = read_files(
        Path("data") / "wordle-allowed-guesses.txt",
        Path("data") / "wordle-answers-alphabetical.txt",
    )

    shuffle(answers)

    with Pool() as p:
        game_lengths = p.map(
            partial(play_game, player=Player, allowed_guesses=allowed_guesses), answers
        )

    print()
    print(sum(game_lengths) / len(game_lengths))
    print(max(game_lengths))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--player", choices=['random', 'valid', 'entropy'], default='valid')
    main(**vars(parser.parse_args()))
