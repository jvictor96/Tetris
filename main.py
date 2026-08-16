import enum
import random
import threading
import time
import asyncio
import subprocess

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
        self.schema = schema

    def rotate(self) -> Piece:
        for block in range(len(self.blocks)):
            self.blocks[block] = (self.blocks[block][1], -self.blocks[block][0])
        return self

    def destroy(self) -> list[tuple[int, int]]:
        return [(x + self.position_x, y + self.position_y) for x, y in self.blocks]

    def clone(self, dx: int, dy:int) -> Piece:
        p = Piece(self.schema)
        p.blocks = [(block[0], block[1]) for block in self.blocks]
        p.position_y = self.position_y+dy
        p.position_x = self.position_x+dx
        return p

def new_piece() -> Piece:
    return Piece(rand_pool[random.randint(0,5)])

class Board:
    def __init__(self):
        self.piece = new_piece()
        self.blocks:list[tuple[int, int]] = []

    def collide(self, piece:Piece)->bool:
        ret = False
        for block in piece.blocks:
            block = (block[0] + piece.position_x, block[1] + piece.position_y)
            ret = ret or block in self.blocks
            ret = ret or block[1] == 20
            ret = ret or block[1] == 0
            ret = ret or block[0] == 10 
            ret = ret or block[0] == 0
        return ret

    def fall(self):
        if self.collide(self.piece.clone(0,1)):
            self.blocks.extend(self.piece.destroy())
            if self.piece.position_y == 2:
                self.blocks = []
            self.piece = new_piece()
            return
        self.piece.position_y += 1

    def draw(self):
        print("--"*11)
        display = ["|" + "  "*10 + "|" for i in range(20)]
        for block in self.blocks:
            display[block[1]] = display[block[1]][:block[0]*2] + "⣿⣿" + display[block[1]][block[0]*2+2:]
        for block in self.piece.destroy():
            display[block[1]] = display[block[1]][:block[0]*2] + "⣿⣿" + display[block[1]][block[0]*2+2:]
        for line in display:
            print(line)
        print("--"*11)

    def read_input(self, inpute):
        if len(inpute) == 0:
            return
        match inpute[-1]:
            case "a":
                if self.collide(self.piece.clone(-1,0)):
                    return
                self.piece.position_x -= 1
            case "w":
                if self.collide(self.piece.clone(0,0).rotate()):
                    return
                self.piece.rotate()
            case "d":
                if self.collide(self.piece.clone(1,0)):
                    return
                self.piece.position_x += 1


board = Board()
def read_input(board_p: Board):
    while True:
        board_p.read_input(input())

def read_input_a():
    asyncio.run(read_input(board))

threading.Thread(target=read_input_a, daemon=True).start()
while True:
    time.sleep(0.4)
    subprocess.run("clear")
    board.fall()
    board.draw()