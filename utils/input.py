def read_files(f1: str, f2: str) -> tuple[list[str], list[str]]:

    with open(f1) as f:
        guesses = f.readlines()

    with open(f2) as f:
        answers = f.readlines()

    guesses = list(map(str.strip, guesses))
    answers = list(map(str.strip, answers))
    guesses.extend(answers)
    return guesses, answers


if __name__ == "__main__":
    x, y = read_files("wordle-allowed-guesses.txt", "wordle-answers-alphabetical.txt")
    print(x[:10])
    print(y[:10])
