from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import Optional

import numpy as np

from game import Game
from utils.input import read_files

from players.random_player import RandomPlayer
from players.valid_player import ValidPlayer
from players.entropy_player import EntropyPlayer


def play_game(player, game, verbose=False):
    while not game.is_won:
        guess = player.guess()
        if verbose: print(f"{guess = }")
        feedback = game.guess(guess)
        if verbose: print(f"{feedback = }")
        player.update(feedback)

    return game.n_guesses


def main(player: str, answer: Optional[str], verbose: bool, plot: bool):
    player_class = {
        "random": RandomPlayer,
        "valid": ValidPlayer,
        "entropy": EntropyPlayer,
    }[player]

    allowed_guesses, answers = read_files(
        Path("data") / "wordle-allowed-guesses.txt",
        Path("data") / "wordle-answers-alphabetical.txt",
    )

    games = [Game([a], allowed_guesses) for a in ([answer] if answer else answers)]
    players = [player_class(vocabulary=answers) for _ in games]

    with Pool() as p:
        game_lengths = p.starmap(partial(play_game, verbose=verbose), zip(players, games))

    game_lengths = np.array(game_lengths)

    print()
    print("MIN:", game_lengths.min())
    print("MAX:", game_lengths.max())
    print("AVG:", game_lengths.mean())
    print("STD:", game_lengths.std())
    print("WIN:", sum(game_lengths <= 6) / len(game_lengths))

    if plot:
        from seaborn import histplot

        ax = histplot(y=game_lengths, binwidth=1, discrete=True)
        ax.set_ylabel("Number of Guesses")
        ax.get_figure().savefig('plot.png')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--player", choices=['random', 'valid', 'entropy'], default='valid')
    parser.add_argument("-a", "--answer")
    parser.add_argument("-v", "--verbose", action='store_true')
    parser.add_argument("-plot", "--plot", action='store_true')
    main(**vars(parser.parse_args()))
