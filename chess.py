import pygame
import numpy as np

RESOLUTION = (600, 600)
SQUARE_SIZE = RESOLUTION[0]/8

pieces = np.array([ 
         4,  2,  3,  6,  5,  3,  2,  4,
         1,  1,  1,  1,  1,  1,  1,  1,
         0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  5,  0,  0,  4,
         0,  0,  0,  0,  -6,  0,  0,  0,
         0,  0,  0,  0,  0,  0,  0,  0,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -4, -2, -3, -6, -5, -3, -2, -4,
])

def drawSquares(screen, selected):
    dark = "#593a1a"
    light = "#b3702e"
    select = '#84b32e'
    for i in range(8):
        for j in range(8):
            color = light if (i+j)%2==0 else dark
            if type(selected) == int and (i, j) == (selected%8, selected//8): color = select
            pygame.draw.rect(screen, color, pygame.Rect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
def drawPieces(screen, pieces):
    # piecelist = pieces[::-1] if PLAYING_AS == 'white' else pieces.copy()
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
            if ctn((i, j)) in findMoves(pieces, selected): pygame.draw.ellipse(screen, move, pygame.Rect(i*SQUARE_SIZE+(SQUARE_SIZE/3), j*SQUARE_SIZE+(SQUARE_SIZE/3), SQUARE_SIZE/3, SQUARE_SIZE/3))
def findMoves(pieces, square):
    if not type(square) == int:
        return []
    moves = []
    if abs(pieces[square]) == 1:
        moves = findPawnMoves(pieces, square, pieces[square])
    if abs(pieces[square]) == 2:
        moves = findKnightMoves(pieces, square)
    if abs(pieces[square]) == 3:
        moves = findBishopMoves(pieces, square)
    if abs(pieces[square]) == 4:
        moves = findRookMoves(pieces, square)
    if abs(pieces[square]) == 5:
        moves = np.union1d(findRookMoves(pieces, square), findBishopMoves(pieces, square))
    if abs(pieces[square]) == 6:
        moves = findKingMoves(pieces, square)
    return moves
    
def findPawnMoves(pieces, square, color):
    moves = []
    if not pieces[square+(1 if color>0 else -1)*8]:
        moves.append(square+(1 if color>0 else -1)*8)
        if (not pieces[square+(1 if color>0 else -1)*16]) and square//8 in [1, 6]:
            moves.append(square+(1 if color>0 else -1)*16)
    if pieces[square+(1 if color>0 else -1)*7] * color < 0:
        moves.append(square+(1 if color>0 else -1)*7)
    if pieces[square+(1 if color>0 else -1)*9] * color < 0:
        moves.append(square+(1 if color>0 else -1)*9)
    return moves
def findKnightMoves(pieces, square):
    moves = []
    knightmoves = [6, 10, 15, 17]
    for i in knightmoves:
        if square + i < 64:
            moves.append(square + i)
        if square - i > 0:
            moves.append(square - i)
    for i in moves.copy():
        if abs(square%8-i%8) > 2 or pieces[i] * pieces[square] > 0:
            moves.remove(i)
    return moves
def findBishopMoves(pieces, square):
    moves = []
    steps = [(1, 1),(1, -1),(-1, 1),(-1, -1)]
    for dx, dy in steps:
        s = 1
        while True:
            try_move = ctn((ntc(square)[1]+dx*s, ntc(square)[0]+dy*s))
            if not (squareColor(square) == squareColor(try_move)):
                break
            elif not isOnBoard(try_move):
                break
            elif pieces[try_move]:
                if pieces[try_move] * pieces[square] < 0:
                    moves.append(try_move)
                    break
                else:
                    break
            else:
                moves.append(try_move)
            s+=1
        try_move = ctn((ntc(square)[0]+dx*s, ntc(square)[1]+dy*s))
    return moves
def findRookMoves(pieces, square):
    moves = []
    steps = [(0, 1),(1, 0),(-1, 0),(0, -1)]
    for dx, dy in steps:
        s = 1
        while True:
            try_move = ctn((ntc(square)[1]+dx*s, ntc(square)[0]+dy*s))
            if try_move%8-square%8 != dx*s or try_move//8-square//8 != dy*s:
                break
            if not isOnBoard(try_move):
                break
            elif pieces[try_move]:
                if pieces[try_move] * pieces[square] < 0:
                    moves.append(try_move)
                    break
                else:
                    break
            else:
                moves.append(try_move)
            s+=1
        try_move = ctn((ntc(square)[0]+dx*s, ntc(square)[1]+dy*s))
    return moves
def findKingMoves(pieces, square):
    moves = []
    for i in range(-8, 16, 8):
        for j in range(-1, 2):
            try_move = square + i + j
            if i==j==0:
                continue
            if not isOnBoard(try_move):
                continue
            if abs(square%8-try_move%8) > 1 or pieces[try_move] * pieces[square] > 0:
                continue
            moves.append(try_move)
    return moves
def ntc(num): # Square Number to Coordinates
    coord = (num//8, num%8)
    return coord
def ctn(coords): # Coordinates to Square Number
    num = coords[1]*8 + coords[0]
    return num
def isOnBoard(square):
    return 0<=square<=63
def isOnEdge(square):
    return square%8 in [0, 7] or square//8 in [0,7]
def squareColor(square):
    return 'white' if (ntc(square)[0] + ntc(square)[1]) % 2 == 0 else 'black'

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
            new_square = int(mpos[1]//SQUARE_SIZE*8 + mpos[0]//SQUARE_SIZE)
            if new_square == selected_square:
                new_square = None
            selected_square = new_square

    drawSquares(screen, selected_square)
    drawPieces(screen, pieces)
    drawMoves(screen, selected_square)

    clock.tick(60)
    pygame.display.update()