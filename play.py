import json
from datetime import datetime
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Optional

import numpy as np

from game import Game
from utils.input import read_files

from players.random_player import RandomPlayer
from players.valid_player import ValidPlayer
from players.entropy_player import EntropyPlayer


def log_to_file(file: Path, **kwargs: dict[str, Any]) -> None:
    with open(file, "a") as f:
        f.write(json.dumps(kwargs) + "\n")


def play_game(player, game, verbose=False):
    while not game.is_won:
        guess = player.guess()
        if verbose: print(f"{guess = }")
        feedback = game.guess(guess)
        if verbose: print(f"{feedback = }")
        player.update(feedback)

    return game.n_guesses


def main(player: str, answer: Optional[str], verbose: bool):
    date_and_time = str(datetime.now())
    open(date_and_time + ".ndjson", "w").close()

    player_classes = {
        "random": [RandomPlayer],
        "valid": [ValidPlayer],
        "entropy": [EntropyPlayer],
        "all": [RandomPlayer, ValidPlayer, EntropyPlayer],
    }[player]

    allowed_guesses, answers = read_files(
        Path("data") / "wordle-allowed-guesses.txt",
        Path("data") / "wordle-answers-alphabetical.txt",
    )

    games = [Game([a], allowed_guesses) for a in ([answer] if answer else answers)]

    for player_class in player_classes:
        player_name = player_class.__name__

        for player_vocab_str, player_vocab in ("allowed", allowed_guesses), ("answers", answers):
            players = [player_class(vocabulary=player_vocab) for _ in games]

            with Pool() as p:
                game_lengths = p.starmap(partial(play_game, verbose=verbose), zip(players, games))

            for game, game_length in zip(games, game_lengths):
                log_to_file(
                    date_and_time + ".ndjson",
                    player=player_name,
                    vocabulary=player_vocab_str,
                    word=game.answer,
                    game_length=game_length,
                )

            game_lengths = np.array(game_lengths)

            print()
            print(player_name)
            print(len(player_name) * "=")
            print("VOC:", player_vocab_str)
            print()
            print("MIN:", game_lengths.min())
            print("MAX:", game_lengths.max())
            print("AVG:", game_lengths.mean())
            print("STD:", game_lengths.std())
            print("WIN:", sum(game_lengths <= 6) / len(game_lengths))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--player", choices=['random', 'valid', 'entropy', 'all'], default='all')
    parser.add_argument("-a", "--answer")
    parser.add_argument("-v", "--verbose", action='store_true')
    main(**vars(parser.parse_args()))
