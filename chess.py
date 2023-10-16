import pygame
from piece import Piece

def drawBoard(screen):
    white = '#ffffff'
    black = '#006600'
    screen.fill('#002000')
    pygame.draw.rect(screen, 'white', pygame.rect.Rect(0, 100, 600, 600))
    for i in range(64):
        if i%2==0 and (i//8)%2==0 or i%2==1 and (i//8)%2==1:
            color = white
        else:
            color = black
        pygame.draw.rect(screen, color, pygame.rect.Rect(75*(i%8), 100+75*(i//8), 75, 75))
def generatePieces(board):
    pieces = pygame.sprite.Group()
    for y, row in enumerate(board):
        for x, square in enumerate(row):
            if square:
                pieces.add(Piece(square[0], square[1], [x, y]))
    return pieces

STARTINGBOARD = [['br','bn','bb','bq','bk','bb','bn','br'],
                 ['bp','bp','bp','bp','bp','bp','bp','bp'],
                 ['','','','','','','',''],
                 ['','','','','','','',''],
                 ['','','','','','','',''],
                 ['','','','','','','',''],
                 ['wp','wp','wp','wp','wp','wp','wp','wp',],
                 ['wr','wn','wb','wq','wk','wb','wn','wr']]

pygame.init()
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()

pieces = generatePieces(STARTINGBOARD)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    drawBoard(screen)
    pieces.draw(screen)
    pieces.update()

    clock.tick(60)
    pygame.display.update()