from typing import Iterable


def is_valid(word: str, last_guess: str, feedback: Iterable[int]) -> bool:
    for i, j, k in zip(word, last_guess, feedback):
        match k:
            case 0:
                if j in word:
                    return False
            case 1:
                if j not in word:
                    return False
                if i == j:
                    return False
            case 2:
                if i != j:
                    return False

    return True
