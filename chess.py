import pygame
import math
import numpy as np

def drawBoard(screen):
    white = '#8080ff'
    black = '#1111ff'
    screen.fill('#ffffff')
    pygame.draw.rect(screen, 'white', pygame.rect.Rect(0, 100, 600, 600))
    for i in range(64):
        if i%2==0 and (i//8)%2==0 or i%2==1 and (i//8)%2==1:
            color = white
        else:
            color = black
        pygame.draw.rect(screen, color, pygame.rect.Rect(75*(i%8), 75*(i//8), 75, 75))

board = [[4, 2, 3, 6, 5, 3, 2, 4],
         [1, 1, 1, 1, 1, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [-1, -1, -1, -1, -1, -1, -1, -1],
         [-4, -2, -3, -6, -5, -3, -2, -4]]
boardhist = []
boardhist.append(board)
turn = 1

def drawPieces(screen, board):
    for y, row in enumerate(board):
        for x, square in enumerate(row):
            if square != 0:
                match square:
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
                img = pygame.transform.scale(pygame.image.load(imgname), (75, 75))
                rect = img.get_rect()
                rect.topleft = (x*75, y*75)
                screen.blit(img, rect)

def highlightSquare(position, color):
    pygame.draw.rect(screen, color, pygame.Rect(position[0]*75, position[1]*75, 75, 75))

def getPos(position):
    return (position[0]//75, position[1]//75)

def getPiece(position):
    if 0<=position[0]<=7 and 0<=position[1]<=7:
        return board[position[1]][position[0]]
    else: return 0

def getMoves(piece, position):
    moves = []
    if abs(piece) == 1:
        if not getPiece(changecoord(position, 0, piece)):
            moves.append(changecoord(position, 0, piece))
            if position[1] in [1, 6] and not getPiece(changecoord(position, 0, piece*2)):
                moves.append(changecoord(position, 0, piece*2))
        if getPiece(changecoord(position, -1, piece)) * piece < 0:
            moves.append(changecoord(position, -1, piece))
        if getPiece(changecoord(position, 1, piece)) * piece < 0:
            moves.append(changecoord(position, 1, piece))
            
    elif abs(piece) == 2:
        for i in [-2, -1, 1, 2]:
            for j in [-2, -1, 1, 2]:
                if abs(i) != abs(j):
                    moves.append((position[0]+i, position[1]+j))
    elif abs(piece) == 3:
        for i in range(max(distToEdge(position))):
            moves.append((position[0]+i, position[1]+i))
            moves.append((position[0]-i, position[1]+i))
            moves.append((position[0]+i, position[1]-i))
            moves.append((position[0]-i, position[1]-i))
    elif abs(piece) == 4:
        for i in range(max(distToEdge(position))):
            moves.append((position[0]+i, position[1]))
            moves.append((position[0]-i, position[1]))
            moves.append((position[0], position[1]+i))
            moves.append((position[0], position[1]-i))
    elif abs(piece) == 5:
        for i in range(max(distToEdge(position))):
            moves.append((position[0]+i, position[1]))
            moves.append((position[0]-i, position[1]))
            moves.append((position[0], position[1]+i))
            moves.append((position[0], position[1]-i))
            moves.append((position[0]+i, position[1]+i))
            moves.append((position[0]-i, position[1]+i))
            moves.append((position[0]+i, position[1]-i))
            moves.append((position[0]-i, position[1]-i))
    elif abs(piece) == 6:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not i==j==0:
                    moves.append(changecoord(position, i, j))
    return [move for move in moves if 0<=move[0]<=7 
            and 0<=move[1]<=7 
            and getPiece(move) * piece <= 0]

def highlightMoves(moves):
    for move in moves:
        highlightSquare(move, 'orange')

def coordToNum(coord):
    return coord[1]*8 + coord[0]
def numToCoord(num):
    return (num%8, num//8)
def movePiece(board, start, end, turn):
    if end in getMoves(getPiece(start), start) and turn*getPiece(start)>=0:
        board[end[1]][end[0]] = board[start[1]][start[0]]
        board[start[1]][start[0]] = 0
        turn *= -1
        boardhist.append(board)
    return board, turn
def distToEdge(pos):
    return [pos[1], 8-pos[1], pos[0], 9-pos[0]]
def changecoord(pos, changex, changey):
    return (pos[0]+changex, pos[1]+changey)
def findPiecesInWay(start, moves, piece):
    for move in moves:
        if np.subtract(move, start)[0] and np.subtract(move, start)[1]:
            for i in range(abs(np.subtract(move, start)[0])):
                if getPiece((start[0]+i,start[1]+i))

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

squareClicked = None
pieceSelected = None
while True:
    drawBoard(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (pygame.mouse.get_pos()[0]//75, pygame.mouse.get_pos()[1]//75) != squareClicked:
                if pieceSelected:
                    board, turn = movePiece(board, squareClicked, (pygame.mouse.get_pos()[0]//75, pygame.mouse.get_pos()[1]//75), turn)
                squareClicked = (pygame.mouse.get_pos()[0]//75, pygame.mouse.get_pos()[1]//75)
                pieceSelected = getPiece(squareClicked)
            else:
                squareClicked = None
                pieceSelected = None
    if squareClicked:
        highlightSquare(squareClicked, 'green')
    if pieceSelected and pieceSelected * turn >= 0:
        highlightMoves(getMoves(pieceSelected, squareClicked))
    drawPieces(screen, board)

    clock.tick(60)
    pygame.display.update()