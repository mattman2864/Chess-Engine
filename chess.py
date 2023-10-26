import pygame
import numpy as np

# Constants
RESOLUTION = (600, 600)
SQUARE_SIZE = RESOLUTION[0]/8
PLAYING_AS = "white"
STARTING_BOARD = np.array([ 
         4,  2,  3,  6,  5,  3,  2,  4,
         1,  1,  1,  1,  1,  1,  1,  1,
         0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  0,  0,  0,  0,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -4, -2, -3, -6, -5, -3, -2, -4,
])
TEST_BOARD = np.array([
    3, 0, 4, 0, -3, 0, 0, 5,
    6, -4, 0, 0, 6, 0, 0, 0,
    3, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 5, 0, 0, 0, 0,
    -3, -6, 0, 0, 3, 0, 6, 0,
    -5, 3, 6, 0, 0, 0, 0, 0,
    4, -6, 0, 0, -3, 0, 0, 0,
    4, 0, 0, 0, 0, 0, 5, 6,
])


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
def drawMoves(screen, moves):
    move_color = "#ff0000"
    for move in moves:
        if PLAYING_AS == "white":
            move = 63 - move
        pygame.draw.ellipse(screen, move_color, pygame.Rect(move%8*SQUARE_SIZE+0.3*SQUARE_SIZE, move//8*SQUARE_SIZE+.3*SQUARE_SIZE, SQUARE_SIZE*.4, SQUARE_SIZE*.4))
def findMoves(board, square):
    if board[square] * turn < 1:
        return []
    piece = board[square]
    moves = []
    match abs(piece):
        case 1:
            moves += getPawnMoves(board, square)
        case 2:
            moves += getKnightMoves(board, square)
        case 3:
            moves += getBishopMoves(board, square)
        case 4:
            moves += getRookMoves(board, square)
        case 5:
            moves += getRookMoves(board, square) + getBishopMoves(board, square)
        case 6:
            moves += getKingMoves(board, square)
    return moves
def getPawnMoves(board, square):
    moves = []
    piece = board[square]
    if abs(square // 8 - 3.5) - 2.5 == 0:
        moves.append(square + 16 * piece)
    moves.append(square + 8 * piece)
    if board[square + 7 * piece] * piece < 0 or square + 7 * piece == en_passant_square:
        moves.append(square + 7 * piece)
    if board[square + 9 * piece] * piece < 0 or square + 9 * piece == en_passant_square:
        moves.append(square + 9 * piece)
    moves = [move for move in moves if 0<=move<=63 and abs(move%8-square%8) <= 2]
    return moves
def getAllPieces(board):
    squares = []
    for i in range(63):
        if board[i]:
            squares.append(i)
    return squares
def getKnightMoves(board, square):
    moves = []
    for i in [6, 10, 15, 17]:
        moves += [square + i, square-i]
    moves = [move for move in moves if 0 <= move <= 63 and board[move]*board[square]<=0 and abs(move%8-square%8) <= 2]
    return moves
def getBishopMoves(board, square):
    moves = []
    i = 1
    dirs = [9, -9, 7, -7]
    while dirs:
        for dir in dirs.copy():
            checkmove = square + dir * i
            if (checkmove+(checkmove//8))%2 != (square+(square//8))%2:
                dirs.remove(dir)
            elif not 0 <= checkmove <= 63:
                dirs.remove(dir)
            elif board[checkmove] * board[square] > 0:
                dirs.remove(dir)
            elif board[checkmove] * board[square] < 0:
                dirs.remove(dir)
                moves.append(checkmove)
            else:
                moves.append(checkmove)
        i += 1
    return moves
def getRookMoves(board, square):
    moves = []
    i = 1
    dirs = [1, -1, 8, -8]
    while len(dirs):
        for dir in dirs.copy():
            checkmove = square + dir * i
            if  not 0 <= checkmove <= 63:
                dirs.remove(dir)
            elif board[checkmove] * board[square] > 0 or not ((square//8!=checkmove//8 and not square%8!=checkmove%8) or (not square//8!=checkmove//8 and square%8!=checkmove%8)):
                dirs.remove(dir)
            elif board[checkmove] * board[square] < 0:
                moves.append(checkmove)
                dirs.remove(dir)
            else:
                moves.append(checkmove)
        i += 1
    return moves
def getKingMoves(board, square):
    moves = []
    for i in [-1, 0, 1]:
        for j in [-8, 0, 8]:
            if i == j == 0:
                continue
            checkmove = square + i + j
            if not 0<=checkmove<=63:
                continue
            if board[checkmove] * board[square] > 0 or abs(checkmove%8-square%8) > 1:
                continue
            moves.append(checkmove)
    if castling[board[square]]:
        if board[square + 1]==0 and board[square + 2]==0 and board[square + 3]==24/board[square]:
            moves.append(square + 2)
    return moves
def makeMove(board, start, end):
    new_board = board.copy()
    new_board[end] = new_board[start]
    new_board[start] = 0
    gamehistory.append(board.copy())
    return new_board

# Pygame
pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

# Initialize Variables
selected_square = None
moves = []
en_passant_square = None
pieces = STARTING_BOARD
gamehistory = []
turn = 1
castling = {6:True, 12:True, -6:True, -12:True}

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
            if new_square in moves:
                pieces = makeMove(pieces, selected_square, new_square)
                turn *= -1
                new_square = None
            elif new_square == selected_square:
                new_square = None
            if type(new_square) == int:
                moves = findMoves(pieces, new_square)
            else:
                moves = []
            selected_square = new_square

    drawSquares(screen)
    if type(selected_square) == int:
        drawSelectedSquares(screen, selected_square)
    drawPieces(screen, pieces)
    drawMoves(screen, moves)

    clock.tick(60)
    pygame.display.update()