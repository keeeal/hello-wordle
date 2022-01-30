from pathlib import Path

class Keyboard:
    def __init__(self) -> None:
        with open(Path("data") / "keyboard.txt",'r') as f:
            board = f.readlines()

        self.board = list(map(str.strip, board))
       # self.status = length(readlines)

    
   # def update(self, feedback, guess):


    #def show(self):




if __name__ == "__main__":
    keyboard = Keyboard()
    print(*keyboard.board,sep="\n")