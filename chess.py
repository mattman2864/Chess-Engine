import pygame
import math

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
    return board[position[1]][position[0]]

def getMoves(piece, position):
    moves = []
    if piece == -1:
        if position[1] == 6:
            moves = [(position[0], position[1]-1), (position[0], position[1]-2)]
        else:
            moves = [(position[0], position[1]-1)]
    elif piece == 1:
        if position[1] == 1:
            moves = [(position[0], position[1]+1), (position[0], position[1]+2)]
        else:
            moves = [(position[0], position[1]+1)]
    elif abs(piece) == 2:
        for i in [-2, -1, 1, 2]:
            for j in [-2, -1, 1, 2]:
                if abs(i) != abs(j):
                    moves.append((position[0]+i, position[1]+j))
    elif abs(piece) == 3:
        pass
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
    if end in getMoves(getPiece(start), start):
        board[end[1]][end[0]] = board[start[1]][start[0]]
        board[start[1]][start[0]] = 0
        turn *= -1
    return board, turn

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
                print(squareClicked, pieceSelected, getMoves(pieceSelected, squareClicked))
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