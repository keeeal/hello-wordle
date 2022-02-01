import json
from datetime import datetime
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Optional

from pandas import DataFrame

from game import Game
from utils.input import read_files

from players.random_player import RandomPlayer
from players.valid_player import ValidPlayer
from players.entropy_player import EntropyPlayer


def log_to_file(file: Path, **kwargs: dict[str, Any]) -> None:
    with open(file, "a") as f:
        f.write(json.dumps(kwargs) + "\n")


def play_game(player, game: Optional[Game], verbose: bool):
    while True:
        guess = player.guess()

        if verbose:
            print(f"{guess = }")

        if game:
            feedback = game.guess(guess)
        else:
            while True:
                try:
                    feedback = list(map(int, input().split()))
                    assert len(feedback) == 5
                    assert all(i in (0, 1, 2) for i in feedback)
                except (ValueError, AssertionError):
                    print(f"Invalid feedback.")
                else:
                    break

        if verbose:
            print(f"{feedback = }")

        player.update(feedback)

        if game and game.is_won:
            return game.n_guesses


def test(
    player: str,
    vocabulary: str,
    answer: Optional[str],
    interactive: bool,
    verbose: bool,
):
    date_and_time = str(datetime.now()) \
        .replace(" ", "-").replace(":", "-").replace(".", "-")
    open(date_and_time + ".ndjson", "w").close()

    allowed, answers = read_files(
        Path("data") / "wordle-allowed-guesses.txt",
        Path("data") / "wordle-answers-alphabetical.txt",
    )

    player_class = {
        "random": RandomPlayer,
        "valid": ValidPlayer,
        "entropy": EntropyPlayer,
    }[player]

    player_vocab = {
        "answers": answers,
        "allowed": allowed
    }[vocabulary]

    if interactive:
        game_lengths = [play_game(player_class(vocabulary=player_vocab), None, True)]
    else:
        games = [Game([a], allowed) for a in ([answer] if answer else answers)]
        players = [player_class(vocabulary=player_vocab) for _ in games]

        with Pool() as p:
            game_lengths = p.starmap(
                partial(play_game, verbose=verbose), zip(players, games)
            )

    for game, game_length in zip(games, game_lengths):
        log_to_file(
            date_and_time + ".ndjson",
            player=player,
            vocabulary=vocabulary,
            word=game.answer,
            game_length=game_length,
        )

    print()
    print(f"{player = }")
    print(f"{vocabulary = }")
    print()
    print(DataFrame(game_lengths, columns=["game_lengths"]).describe())
    print()
    print(f"win_percent = {sum(i <= 6 for i in game_lengths) / len(game_lengths) :.2%}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--player", choices=["random", "valid", "entropy"], default="entropy")
    parser.add_argument("-voc", "--vocabulary", choices=["answers", "allowed"], default="answers")
    parser.add_argument("-a", "--answer")
    parser.add_argument("-i", "--interactive", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    test(**vars(parser.parse_args()))
