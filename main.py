import enum
import random
import threading
import time
import asyncio
import subprocess

class Block:
    def __init__(self, x:int, y:int):
        self.y = y
        self.x = x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Schemas(enum.Enum):
    L = [Block(2,0),Block(1,0),Block(0,0),Block(0,1)]
    T = [Block(2,0),Block(1,0),Block(0,0),Block(1,1)]
    N = [Block(0,0),Block(1,0),Block(1,1),Block(2,1)]
    NR = [Block(0,0),Block(0,1),Block(1,1),Block(1,2)]
    Q = [Block(0,0),Block(1,0),Block(1,1),Block(0,1)]
    I = [Block(0,0),Block(0,1),Block(0,2),Block(0,3)]

rand_pool = [Schemas.L, Schemas.T, Schemas.N, Schemas.NR, Schemas.Q, Schemas.I]

class Piece:
    def __init__(self, schema: Schemas):
        self.position_x = 5
        self.position_y = 2
        self.blocks = schema.value
        self.schema = schema

    def rotate(self) -> Piece:
        for block in range(len(self.blocks)):
            self.blocks[block].x, self.blocks[block].y = self.blocks[block].y, -self.blocks[block].x
        return self

    def destroy(self) -> list[Block]:
        return [Block(block.x + self.position_x, block.y + self.position_y) for block in self.blocks]

    def clone(self, dx: int, dy:int) -> Piece:
        p = Piece(self.schema)
        p.blocks = [Block(block.x, block.y) for block in self.blocks]
        p.position_y = self.position_y+dy
        p.position_x = self.position_x+dx
        return p

def new_piece() -> Piece:
    return Piece(rand_pool[random.randint(0,5)])

class Board:
    def __init__(self):
        self.piece = new_piece()
        self.blocks:list[Block] = []

    def verify(self):
        check:list[list[Block]] = [[] for i in range(20)]
        for block in self.blocks:
            check[block.y].append(block)
        for i, result in enumerate(check):
            if len(result) == 9:
                [self.blocks.remove(block) for block in result]
                for j in range(i-1, -1, -1):
                    for k in range(len(check[j])):
                        check[j][k].y += 1



    def collide(self, piece:Piece)->bool:
        ret = False
        for block in piece.blocks:
            block = Block(block.x + piece.position_x, block.y + piece.position_y)
            ret = ret or block in self.blocks
            ret = ret or block.y == 20
            ret = ret or block.y == 0
            ret = ret or block.x == 10 
            ret = ret or block.x == 0
        return ret

    def fall(self):
        if self.collide(self.piece.clone(0,1)):
            self.blocks.extend(self.piece.destroy())
            self.verify()
            if self.piece.position_y == 2:
                self.blocks = []
            self.piece = new_piece()
            return
        self.piece.position_y += 1

    def draw(self):
        print("--"*11)
        display = ["|" + "  "*10 + "|" for i in range(20)]
        for block in self.blocks:
            display[block.y] = display[block.y][:block.x*2] + "⣿⣿" + display[block.y][block.x*2+2:]
        for block in self.piece.destroy():
            display[block.y] = display[block.y][:block.x*2] + "⣿⣿" + display[block.y][block.x*2+2:]
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