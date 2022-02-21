from json import load
from pathlib import Path


def load_words(*files: Path) -> list[str]:
    words = set()

    for file in files:
        with open(file) as f:
            words.update(map(str.strip, f.readlines()))

    return sorted(words)


def load_frequencies(*files: Path) -> dict[str, float]:
    freqs = dict()

    for file in files:
        with open(file) as f:
            freqs.update(load(f))

    return freqs
