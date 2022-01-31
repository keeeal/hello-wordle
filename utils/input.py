from pathlib import Path

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
    x, y = read_files(Path("data") / "wordle-allowed-guesses.txt", Path("data") / "wordle-answers-alphabetical.txt")
    print(x[:10])
    print(y[:10])

    print("words with repeated letter")
    bigcount = 0
    for word in y:
        count = {}
        for s in word:
            if s in count:
                count[s] += 1
                bigcount +=1
                print(word)
                break
            else:
                count[s] = 1
    
    print(bigcount)
    print(bigcount/len(y))
    
