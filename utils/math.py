from math import log, exp


def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))


def normalise_frequencies(
    vocabulary: dict[str, float], scale: float
) -> dict[str, float]:
    words, freqs = zip(*vocabulary.items())
    inv_freqs = [1 - f for f in freqs]
    alpha = 1 + len(inv_freqs) / sum(map(log, inv_freqs))
    lin_inv_freqs = [pow(f, -alpha) for f in inv_freqs]
    lin_freqs = [1 - f for f in lin_inv_freqs]
    mean_lin_freq = sum(lin_freqs) / len(lin_freqs)
    lin_freqs = [scale * (f - mean_lin_freq) for f in lin_freqs]
    return dict(zip(words, map(sigmoid, lin_freqs)))
