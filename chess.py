import pygame

RESOLUTION = (600, 600)
SQUARE_SIZE = RESOLUTION[0]/8

pieces = [ 
        4,  2,  3,  6,  5,  3,  2,  4,
        1,  1,  1,  1,  1,  1,  1,  1,
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -4, -2, -3, -6, -5, -3, -2, -4,
]

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
            selected_square = int(mpos[1]//SQUARE_SIZE*8 + mpos[0]//SQUARE_SIZE)
            print(selected_square)

    drawSquares(screen, selected_square)
    drawPieces(screen, pieces)

    clock.tick(60)
    pygame.display.update()