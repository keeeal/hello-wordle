from string import Template, ascii_lowercase
from typing import Iterable


layout = Template(
"""
[$q][$w][$e][$r][$t][$y][$u][$i][$o][$p]
 [$a][$s][$d][$f][$g][$h][$j][$k][$l]
   [$z][$x][$c][$v][$b][$n][$m]
"""
)

colours = [
    "\u001b[30;1m",  # grey
    "\u001b[33;1m",  # yellow
    "\u001b[32;1m",  # green
    "\u001b[0m",     # reset
]


class Keyboard:
    def __init__(self) -> None:
        self.letters = dict.fromkeys(ascii_lowercase, -1)

    def __str__(self) -> str:
        return layout.substitute(
            {
                letter: colours[value] + letter + colours[-1]
                for letter, value in self.letters.items()
            }
        )

    def update(self, last_guess: str, feedback: Iterable[int]) -> None:
        for letter, value in zip(last_guess, feedback):
            self.letters[letter] = max(self.letters[letter], value)
