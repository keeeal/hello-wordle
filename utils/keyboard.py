from pathlib import Path

class Keyboard:
    def __init__(self) -> None:
        with open(Path("data") / "keyboard.txt",'r') as f:
            board = f.readlines()

        self.board = list(map(str.strip, board))




if __name__ == "__main__":
    keyboard = Keyboard()
    print(*keyboard.board,sep="\n")