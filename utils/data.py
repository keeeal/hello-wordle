from pathlib import Path


def load_words(*files: Path) -> list[str]:
    words = set()

    for file in files:
        with open(file) as f:
            words.update(map(str.strip, f.readlines()))

    return sorted(words)
