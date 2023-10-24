import pygame
import numpy as np

RESOLUTION = (600, 600)
SQUARE_SIZE = RESOLUTION[0]/8
PLAYING_AS = "white"
pieces = np.array([ 
         4,  2,  3,  6,  5,  3,  2,  4,
         1,  1,  1,  1,  1,  1,  1,  1,
         0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  0,  0,  0,  0,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -4, -2, -3, -6, -5, -3, -2, -4,
])
turn = 1

def drawSquares(screen):
    dark = "#593a1a"
    light = "#b3702e"
    for row in range(8):
        for col in range(8):
            color = light if (row + col)%2==0 else dark
            pygame.draw.rect(screen, color, pygame.Rect(row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
def drawSelectedSquares(screen, square):
    select = "#84b32e"
    if PLAYING_AS == "black":
        row, col = square//8, square%8
    else:
        row, col = 7-square//8, 7-square%8
    pygame.draw.rect(screen, select, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
def drawPieces(screen, pieces):
    pieces = np.flip(pieces) if PLAYING_AS == "white" else pieces
    for i, piece in enumerate(pieces):
        if not piece: continue
        match piece:
            case 1:
                imgname='icons/wp.png'
            case 2:
                imgname='icons/wn.png'
            case 3:
                imgname='icons/wb.png'
            case 4:
                imgname='icons/wr.png'
            case 5:
                imgname='icons/wq.png'
            case 6:
                imgname='icons/wk.png'
            case -1:
                imgname='icons/bp.png'
            case -2:
                imgname='icons/bn.png'
            case -3:
                imgname='icons/bb.png'
            case -4:
                imgname='icons/br.png'
            case -5:
                imgname='icons/bq.png'
            case -6:
                imgname='icons/bk.png'
        img = pygame.transform.scale(pygame.image.load(imgname), (SQUARE_SIZE, SQUARE_SIZE)).convert_alpha()
        rect = img.get_rect()
        rect.topleft = (i%8*SQUARE_SIZE,i//8*SQUARE_SIZE)
        screen.blit(img, rect)
def drawMoves(screen, selected):
    move = "#ff0000"
    for i in range(8):
        for j in range(8):
            if i*8+j in findMoves(pieces, selected, True): pygame.draw.ellipse(screen, move, pygame.Rect(i*SQUARE_SIZE+(SQUARE_SIZE/3), j*SQUARE_SIZE+(SQUARE_SIZE/3), SQUARE_SIZE/3, SQUARE_SIZE/3))
def findMoves(board):
    pieces = getAllPieces(board)
    print(pieces)
def getAllPieces(board):
    squares = []
    for i in range(63):
        if board[i]:
            squares.append(i)
    return squares


pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
selected_square = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if PLAYING_AS == "black":
                new_square = int(mpos[1]//SQUARE_SIZE*8 + mpos[0]//SQUARE_SIZE)
            else:
                new_square = 63-int(mpos[1]//SQUARE_SIZE*8 + mpos[0]//SQUARE_SIZE)
            if new_square == selected_square:
                new_square = None
            selected_square = new_square

    drawSquares(screen)
    if type(selected_square) == int:
        drawSelectedSquares(screen, selected_square)
    drawPieces(screen, pieces)

    clock.tick(60)
    pygame.display.update()