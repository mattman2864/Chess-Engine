import numpy as np
import pygame as pg

# Settings
BOARD_SIZE = 600 # Pixels


WHITE = 'white'
BLACK = 'black'
SQUARE_SIZE = BOARD_SIZE/8
RESOLUTION = (BOARD_SIZE, BOARD_SIZE)

class Board:
    def __init__(self, side: str):
        self.side = side
        self.board = np.array([
            4, 2, 3, 6, 5, 3, 2, 4,
            1, 1, 1, 1, 1, 1, 1, 1,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1, 1,
            4, 2, 3, 6, 5, 3, 2, 4
        ])
    def drawBoard(screen):
        dark = "#593a1a"
        light = "#b3702e"
        for i in range(8):
            for j in range(8):
                color = light if (i+j)%2==0 else dark
                pg.draw.rect(screen, color, pg.Rect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    def drawSelectedSquares(screen, square):
        select = "#84b32e"
        x, y = ntc(square)
        pg.draw.rect(screen, select, pg.Rect(x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

turn = WHITE
selected_square = None

pg.init()
screen = pg.display.set_mode(RESOLUTION)
clock = pg.time.Clock()
board = Board(1)

def ntc(num): # Square Number to Coordinates
    coord = (num%8, num//8)
    return coord
def ctn(coords): # Coordinates to Square Number
    num = coords[1]*8 + coords[0]
    return num



while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = pg.mouse.get_pos()
            new_square = int(mpos[1]//SQUARE_SIZE*8 + mpos[0]//SQUARE_SIZE)
            if new_square == selected_square:
                new_square = None
            selected_square = new_square
    board.drawBoard(screen)
    if selected_square != None:
        board.drawSelectedSquares(screen, selected_square)

    clock.tick(60)
    pg.display.update()