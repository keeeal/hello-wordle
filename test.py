from datetime import datetime
from json import dumps
from pathlib import Path
from typing import Optional

from pandas import DataFrame
from tqdm import tqdm

from utils.data import load_frequencies, load_words
from utils.game import Game, Feedback

from players.convnet_player import ConvnetPlayer
from players.entropy_player import EntropyPlayer
from players.mcts_player import MctsPlayer
from players.minimax_player import MinimaxPlayer
from players.valid_player import ValidPlayer
from utils.math import normalise_frequencies


def log_to_file(file: Path, **kwargs) -> None:
    with open(file, "a+") as f:
        f.write(dumps(kwargs) + "\n")


def play_game(player, game: Optional[Game], verbose: bool) -> int:
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
    player_name: str,
    word_list: str,
    first_guess: Optional[str],
    answer: Optional[str],
    interactive: bool,
    verbose: bool,
) -> None:
    date_and_time = str(datetime.now()) \
        .replace(" ", "-").replace(":", "-").replace(".", "-")

    # get player class
    player_class = {
        "convnet": ConvnetPlayer,
        "entropy": EntropyPlayer,
        "mcts": MctsPlayer,
        "minimax": MinimaxPlayer,
        "valid": ValidPlayer,
    }[player_name]

    # load word data
    print("\nLoading data...")

    if word_list == "answers":
        words = load_words(Path("data") / "wordle-answers.txt")
    elif word_list == "all":
        words = load_words(
            Path("data") / "wordle-allowed.txt",
            Path("data") / "wordle-answers.txt",
        )
    else:
        print(f"Invalid word list: {word_list}")
        return

    freq = load_frequencies(Path("data") / "frequencies.json")
    words = {word: freq[word] for word in words}
    words = normalise_frequencies(words, scale=10)
    print(f"{len(words)} words.")

    # create games and players
    print("\nCreating games...")
    if interactive:
        games = [None]
        players = [player_class(words, first_guess)]
        verbose = True
    else:
        games = [Game([a], words) for a in ([answer] if answer else words)]
        players = [player_class(words, first_guess) for _ in games]

    # create log directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / (date_and_time + ".ndjson")

    # play games
    print("\nPlaying...")
    game_lengths = []
    for game, player in zip(tqdm(games), players):
        game_lengths.append(play_game(player, game, verbose))

        log_to_file(
            log_file,
            player=player_name,
            word_list=word_list,
            first_guess=first_guess,
            answer=game.answer,
            game_length=game_lengths[-1],
        )

    print()
    print(f"{player_name = }")
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
        "mcts",
        "minimax",
        "valid",
    ]

    word_lists = [
        "answers",
        "all",
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--player-name", choices=players, default="valid")
    parser.add_argument("-w", "--word-list", choices=word_lists, default="all")
    parser.add_argument("-f", "--first-guess")
    parser.add_argument("-a", "--answer")
    parser.add_argument("-i", "--interactive", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    test(**vars(parser.parse_args()))
