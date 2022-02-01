from functools import partial
import json
from itertools import chain
from pathlib import Path
from typing import Iterator

from pandas import DataFrame, concat
from seaborn import lineplot


def read_log(file: Path, bin: bool = False) -> DataFrame:
    with open(file) as f:
        data = DataFrame(map(json.loads, f.readlines()))

    if bin:
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

        data = DataFrame(binned_data)

    return data


def plot(files: list[Path]) -> None:
    data = concat(map(partial(read_log, bin=True), files), ignore_index=True)

    ax = lineplot(
        data=data,
        x="game_length",
        y="count",
        hue="player",
        style="vocabulary",
    )
    ax.get_figure().savefig("plot.png")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    plot(**vars(parser.parse_args()))
