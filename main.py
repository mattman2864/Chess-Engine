import pygame as pg
from engine import GameState, Move
from numpy import intersect1d

# Constants
resolution = (700, 500)
NUM_SQUARES = 8
square_size = resolution[1]//NUM_SQUARES
font_size = int((20/1000)*resolution[0])

FRAMERATE = 30

TITLE = 'Chess in Python'

LIGHT_COLOR = '#ffffcc'
DARK_COLOR = '#484985'
SELECT_COLOR = '#aaff80'

PIECE_LIST = ['br', 'bn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wn', 'wb', 'wq', 'wk', 'wp']
PIECE_ICONS = {}

def load_pieces():
    for piece in PIECE_LIST:
        PIECE_ICONS[piece] = pg.transform.scale(pg.image.load(f'icons/{piece}.png'), (square_size, square_size))

def draw_squares(screen):
    for r in range(NUM_SQUARES):
        for c in range(NUM_SQUARES):
            color = LIGHT_COLOR if (r+c)%2==0 else DARK_COLOR
            pg.draw.rect(screen, color, pg.Rect(square_size*c, square_size*r, square_size, square_size))

def highlight_square(screen, square):
    if not square:
        return
    pg.draw.rect(screen, SELECT_COLOR, pg.Rect(square[1]*square_size, square[0]*square_size, square_size, square_size))

def draw_pieces(screen, board):
    for row in range(NUM_SQUARES):
        for col in range(NUM_SQUARES):
            if not(0 <= row < len(board) and 0 <= col < len(board[row])):
                continue
            if board[row][col] == '--':
                continue
            screen.blit(PIECE_ICONS[board[row][col]], pg.Rect(col*square_size, row*square_size, square_size, square_size))

def draw_move_list(screen, move_list, undo_list, font: pg.font.Font):
    undo_list.reverse()
    if undo_list:
        total_list = move_list + undo_list
    else:
        total_list = move_list
    for i in range(len(total_list)):
        if i%2 == 0:
            move = f'{i//2+1}. '+str(total_list[i])
        else:
            move = str(total_list[i])
        color = '#ffffff' if i < len(move_list) else '#666666'
        text = font.render(move, True, color)
        text_rect = pg.Rect(int(resolution[1]+(resolution[0]-resolution[1])//2*(i%2)), (i//2)*20, resolution[0]*1/9, font_size)
        screen.blit(text, text_rect)

def draw_watermark(screen, font):
    screen.blit(font.render('github.com/mattman2864', True, '#555555'), pg.Rect(resolution[1], resolution[1]-font_size, resolution[0]-resolution[1], font_size))

def draw_moves(screen, moves):
    for move in moves:
        pg.draw.ellipse(screen, '#ff4444', pg.Rect(move.end_col*square_size + (square_size/3), move.end_row*square_size + (square_size/3), square_size/3, square_size/3))

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

if __name__ == "__main__":
    load_pieces()
    pg.init()
    screen = pg.display.set_mode(resolution, pg.RESIZABLE)
    clock = pg.time.Clock()
    moves_font = pg.font.Font('font.ttf', font_size)
    pg.display.set_caption(TITLE)
    pg.display.set_icon(PIECE_ICONS['bp'])

    running = True
    selected_square = ()
    game_state = GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False
    local_moves = []

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                new_row = pg.mouse.get_pos()[1]//square_size
                new_col = pg.mouse.get_pos()[0]//square_size
                if new_col >= NUM_SQUARES:
                    continue
                if (new_row, new_col) == selected_square:
                    selected_square = ()
                else:
                    if selected_square and game_state.board[selected_square[0]][selected_square[1]] != '--':
                        move = Move(selected_square, (new_row, new_col), game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.make_move(valid_moves[i])
                                selected_square = ()
                                move_made = True
                                break
                        selected_square = (new_row, new_col)
                    else:
                        selected_square = (new_row, new_col)
                    local_moves = game_state.get_local_moves(selected_square[0], selected_square[1])
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    game_state.undo_move()
                    move_made = True
                if event.key == pg.K_RIGHT:
                    game_state.redo_move()
                    move_made = True
            if event.type == pg.VIDEORESIZE:
                resolution = (event.w, event.h)
                screen = pg.display.set_mode(resolution, pg.RESIZABLE)
                square_size = resolution[1]//NUM_SQUARES
                font_size = int((20/800)*resolution[1])
                load_pieces()
                moves_font = pg.font.Font('font.ttf', font_size)

        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False
            selected_square = ()

        screen.fill('#111111')
        draw_squares(screen)
        highlight_square(screen, selected_square)
        draw_pieces(screen, game_state.board)
        if selected_square:
            draw_moves(screen, intersection(valid_moves, local_moves))

        draw_move_list(screen, game_state.moves_list, game_state.undo_list.copy(), moves_font)
        draw_watermark(screen, moves_font)

        clock.tick(FRAMERATE)
        pg.display.update()