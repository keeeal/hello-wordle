import json
from pathlib import Path
from typing import Iterator

from pandas import DataFrame
from seaborn import lineplot


def read_log(file: Path) -> Iterator:
    with open(file) as f:
        return map(json.loads, f.readlines())


def plot(file: str) -> None:
    data = DataFrame(read_log(file))
    binned_data = []

    for player in set(data["player"]):
        for vocabulary in set(data["vocabulary"]):
            game_lengths = list(
                data.loc[
                    (data["player"] == player) & (data["vocabulary"] == vocabulary),
                    "game_length",
                ]
            )
            for game_length in set(game_lengths):
                binned_data.append(
                    dict(
                        player=player,
                        vocabulary=vocabulary,
                        game_length=game_length,
                        count=game_lengths.count(game_length),
                    )
                )

    ax = lineplot(
        data=DataFrame(binned_data),
        x="game_length",
        y="count",
        hue="player",
        style="vocabulary",
    )
    ax.get_figure().savefig("plot.png")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    plot(**vars(parser.parse_args()))
