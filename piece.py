import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, color, type, position):
        super().__init__()
        self.color = color
        self.type = type
        self.position = position
        if self.color == 'w':
            match self.type:
                case 'k':
                    imagefile = 'icons/wk.png'
                case 'q':
                    imagefile = 'icons/wq.png'
                case 'b':
                    imagefile = 'icons/wb.png'
                case 'n':
                    imagefile = 'icons/wn.png'
                case 'r':
                    imagefile = 'icons/wr.png'
                case 'p':
                    imagefile = 'icons/wp.png'
        else:
            match self.type:
                case 'k':
                    imagefile = 'icons/bk.png'
                case 'q':
                    imagefile = 'icons/bq.png'
                case 'b':
                    imagefile = 'icons/bb.png'
                case 'n':
                    imagefile = 'icons/bn.png'
                case 'r':
                    imagefile = 'icons/br.png'
                case 'p':
                    imagefile = 'icons/bp.png'
        self.image = pygame.transform.scale(pygame.image.load(imagefile), (75, 75))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position[0]*75, 100+self.position[1]*75)
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.dragging = True
        else:
            self.dragging = False
        if self.dragging:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.rect.topleft = (self.position[0]*75, 100+self.position[1]*75)
    # def mbup(self):
    #     if self.dragging:

    def draw(self, screen):
        screen.blit(self.image, self.rect)