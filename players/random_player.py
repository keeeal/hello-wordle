
from random import shuffle

class RandomPlayer:
    def __init__(self, vocabulary) -> None:
        self.vocabulary = vocabulary
        shuffle(self.vocabulary)
        self.iterator = iter(self.vocabulary)

    def guess(self) -> str:
        return next(self.iterator)

    def update(self, feedback):
        pass
