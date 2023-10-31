import pygame
import ChessEngine

pygame.init()
WIDTH = HEIGHT = 512
DIMENSION = 8 # 8x8 Chess Board
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}

def load_images():
    pieces = ['bb', 'bk', 'bn', 'bp', 'br', 'bq', 'wb', 'wk', 'wn', 'wp', 'wq', 'wr']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("icons/"+piece+".png"), (SQUARE_SIZE, SQUARE_SIZE)).convert_alpha()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False


    load_images()
    square_selected = ()
    moves = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]//SQUARE_SIZE
                row = location[1]//SQUARE_SIZE
                new_square = (row, col)
                if square_selected == new_square:
                    square_selected = ()
                elif square_selected:
                    move = ChessEngine.Move(square_selected, new_square, gs.board)
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        square_selected = ()
                    else:
                        square_selected = new_square
                else:
                    square_selected = new_square
                if square_selected and gs.board[square_selected[0]][square_selected[1]] != '--':
                    moves = intersection(gs.get_valid_moves(), gs.move_functions[gs.board[square_selected[0]][square_selected[1]][1]](square_selected[0], square_selected[1], moves))
                elif not square_selected:
                    moves = []
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gs.undo_move()
                    move_made = True
        
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False


        draw_game_state(screen, gs, square_selected, moves)
        
        clock.tick(MAX_FPS)
        pygame.display.flip()

def draw_game_state(screen, gs, selected, moves):
    draw_board(screen, selected)
    draw_pieces(screen, gs.board)
    draw_moves(screen, gs.board, moves)
def draw_board(screen, selected):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            dark, light = '#B88B4A', '#e3c16f'
            select = '#aaffaa'
            color = light if (row+col)%2==0 else dark
            pygame.draw.rect(screen, color, pygame.Rect(col*SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if (row, col) == selected:
                pygame.draw.rect(screen, select, pygame.Rect(col*SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
def draw_moves(screen, board, moves):
    for move in moves:
        pygame.draw.ellipse(screen, '#ff4444', pygame.Rect(move.end_col*SQUARE_SIZE + (SQUARE_SIZE/3), move.end_row*SQUARE_SIZE + (SQUARE_SIZE/3), SQUARE_SIZE/3, SQUARE_SIZE/3))
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

if __name__ == "__main__":
    main()