from datetime import datetime
from json import dumps
from pathlib import Path
from typing import Any, Optional

from pandas import DataFrame
from tqdm import tqdm

from utils.data import load_words
from utils.game import Game, Feedback

from players.convnet_player import ConvnetPlayer
from players.entropy_player import EntropyPlayer
from players.mcts_player import MctsPlayer
from players.minimax_player import MinimaxPlayer
from players.valid_player import ValidPlayer


def log_to_file(file: Path, **kwargs: dict[str, Any]) -> None:
    with open(file, "a") as f:
        f.write(dumps(kwargs) + "\n")


def play_game(player, game: Optional[Game], verbose: bool):
    while True:
        guess = player.guess()

        if verbose:
            print(f"guess: ||{guess}||")

        if game:
            feedback = game.guess(guess)
        else:
            while True:
                try:
                    feedback = Feedback(map(int, input().split()))
                    assert len(feedback) == 5
                    assert all(i in (0, 1, 2) for i in feedback)
                except (ValueError, AssertionError):
                    print(f"Invalid feedback.")
                else:
                    break

        if verbose:
            print(feedback)

        player.update(feedback)

        if feedback.is_win():
            return len(game.guesses)


def test(
    player: str,
    word_list: str,
    first_guess: Optional[str],
    answer: Optional[str],
    interactive: bool,
    verbose: bool,
):
    date_and_time = str(datetime.now()) \
        .replace(" ", "-").replace(":", "-").replace(".", "-")
    open(date_and_time + ".ndjson", "w").close()

    player_class = {
        "convnet": ConvnetPlayer,
        "entropy": EntropyPlayer,
        "mcts": MctsPlayer,
        "minimax": MinimaxPlayer,
        "valid": ValidPlayer,
    }[player]

    if word_list == "answers":
        words = load_words(Path("data") / "wordle-answers-alphabetical.txt")
    elif word_list == "allowed":
        words = load_words(
            Path("data") / "wordle-allowed-guesses.txt",
            Path("data") / "wordle-answers-alphabetical.txt",
        )
    else:
        print(f"Invalid word list: {word_list}")
        return

    if interactive:
        game_lengths = [play_game(player_class(words, first_guess), None, True)]
    else:
        games = [Game([a], words) for a in ([answer] if answer else words)]
        players = [player_class(words, first_guess) for _ in games]
        game_lengths = [play_game(g, p, verbose) for g, p in zip(tqdm(players), games)]

    for game, game_length in zip(games, game_lengths):
        log_to_file(
            date_and_time + ".ndjson",
            player=player,
            word_list=word_list,
            first_guess=first_guess,
            word=game.answer,
            game_length=game_length,
        )

    print()
    print(f"{player = }")
    print(f"{word_list = }")
    print(f"{first_guess = }")
    print()
    print(DataFrame(game_lengths, columns=["game_lengths"]).describe())
    print()
    print(f"win_percent = {sum(i <= 6 for i in game_lengths) / len(game_lengths) :.2%}")


if __name__ == "__main__":
    import argparse

    players = [
        "convnet",
        "entropy",
        "interaction",
        "mcts",
        "minimax",
        "minimean",
        "valid",
    ]

    word_lists = [
        "answers",
        "allowed"
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--player", choices=players, default="entropy")
    parser.add_argument("-w", "--word-list", choices=word_lists, default="answers")
    parser.add_argument("-f", "--first-guess")
    parser.add_argument("-a", "--answer")
    parser.add_argument("-i", "--interactive", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    test(**vars(parser.parse_args()))
