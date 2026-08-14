import enum
import random
import time


class Schemas(enum.Enum):
    L = [(2,0),(1,0),(0,0),(0,1)]
    T = [(2,0),(1,0),(0,0),(1,1)]
    N = [(0,0),(1,0),(1,1),(2,1)]
    NR = [(0,0),(0,1),(1,1),(1,2)]
    Q = [(0,0),(1,0),(1,1),(0,1)]
    I = [(0,0),(0,1),(0,2),(0,3)]

rand_pool = [Schemas.L, Schemas.T, Schemas.N, Schemas.NR, Schemas.Q, Schemas.I]



class Piece:
    def __init__(self, schema: Schemas):
        self.position_x = 5
        self.position_y = 2
        self.blocks = schema.value

    def rotate(self):
        pass

    def destroy(self) -> list[tuple[int, int]]:
        return [(x + self.position_x, y + self.position_y) for x, y in self.blocks]

def new_piece() -> Piece:
    return Piece(rand_pool[random.randint(0,5)])

class Board:
    def __init__(self):
        self.piece = new_piece()
        self.blocks:list[tuple[int, int]] = []

    def fall(self):
        for block in self.piece.blocks:
            if (block[0]  + self.piece.position_x, block[1] + 1 + self.piece.position_y) in self.blocks or block[1] + 1 + self.piece.position_y == 19:
                self.blocks.extend(self.piece.destroy())
                if self.piece.position_y == 2:
                    self.blocks = []
                self.piece = new_piece()
                return
        self.piece.position_y += 1

    def draw(self):
        print("--"*20)
        display = ["  "*20 + "|" for i in range(20)]
        for block in self.blocks:
            display[block[1]] = display[block[1]][:block[0]*2] + "⣿⣿" + display[block[1]][block[0]*2+2:]
        for block in self.piece.destroy():
            display[block[1]] = display[block[1]][:block[0]*2] + "⣿⣿" + display[block[1]][block[0]*2+2:]
        for line in display:
            print(line)

board = Board()
while True:
    time.sleep(0.2)
    board.fall()
    board.draw()
            