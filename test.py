import json
from datetime import datetime
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Optional

from pandas import DataFrame
from tqdm import tqdm

from game import Game
from utils.input import read_files

from players.convnet_player import ConvnetPlayer
from players.entropy_player import EntropyPlayer
from players.interaction_player import InteractionPlayer
from players.mcts_player import MctsPlayer
from players.minimax_player import MinimaxPlayer
from players.random_player import RandomPlayer
from players.valid_player import ValidPlayer


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
    first_guess: Optional[str],
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
        "convnet": ConvnetPlayer,
        "entropy": EntropyPlayer,
        "interaction": InteractionPlayer,
        "mcts": MctsPlayer,
        "minimax": MinimaxPlayer,
        "random": RandomPlayer,
        "valid": ValidPlayer,
    }[player]

    player_vocab = {
        "answers": answers,
        "allowed": allowed
    }[vocabulary]

    answers = [answer] if answer else answers
    assert len(set(answers).difference(allowed)) == 0

    if interactive:
        game_lengths = [play_game(player_class(player_vocab, first_guess), None, True)]
    else:
        games = [Game([a], allowed) for a in answers]
        players = [player_class(player_vocab, first_guess) for _ in games]

        with Pool() as p:
            game_lengths = p.starmap(
                partial(play_game, verbose=verbose),
                tqdm(zip(players, games), total=len(games)),
            )

    for game, game_length in zip(games, game_lengths):
        log_to_file(
            date_and_time + ".ndjson",
            player=player,
            vocabulary=vocabulary,
            first_guess=first_guess,
            word=game.answer,
            game_length=game_length,
        )

    print()
    print(f"{player = }")
    print(f"{vocabulary = }")
    print(f"{first_guess = }")
    print()
    print(DataFrame(game_lengths, columns=["game_lengths"]).describe())
    print()
    print(f"win_percent = {sum(i <= 6 for i in game_lengths) / len(game_lengths) :.2%}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    players = ["convnet", "entropy", "interaction", "mcts", "minimax", "random", "valid"]
    parser.add_argument("-p", "--player", choices=players, default="entropy")
    parser.add_argument("-voc", "--vocabulary", choices=["answers", "allowed"], default="answers")
    parser.add_argument("-f", "--first-guess")
    parser.add_argument("-a", "--answer")
    parser.add_argument("-i", "--interactive", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    test(**vars(parser.parse_args()))
