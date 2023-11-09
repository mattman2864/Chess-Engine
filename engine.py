from collections.abc import Iterable


class GameState:
    def __init__(self):
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]
        self.moves_list = []
        self.undo_list = []
        self.move_functions = {
            "p": self.get_pawn_moves,
            "n": self.get_knight_moves,
            "b": self.get_bishop_moves,
            "r": self.get_rook_moves,
            "q": self.get_queen_moves,
            "k": self.get_king_moves,
        }
        self.white_to_move = True

    def make_move(self, move):
        self.apply_move(move)
        self.undo_stack_reset()

    def apply_move(self, move):
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moves_list.append(move)
        self.white_to_move = not self.white_to_move
        if move.is_promotion:
            ...
    def undo_move(self):
        if not self.moves_list:
            return
        move = self.moves_list.pop()
        self.undo_list.append(move)
        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.piece_captured
        self.white_to_move = not self.white_to_move

    def redo_move(self):
        if not len(self.undo_list):
            return
        self.apply_move(self.undo_list.pop())

    def undo_stack_reset(self):
        self.undo_list = []

    def get_valid_moves(self):
        moves = self.get_all_moves()
        return moves
    
    def get_all_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                moves += self.get_local_moves(row, col)
        return moves
    
    def get_local_moves(self, row, col):
        turn = self.board[row][col][0]
        if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
            return self.move_functions[self.board[row][col][1]](row, col)
        else:
            return []

    def get_pawn_moves(self, row, col):
        moves = []
        d = 1 if self.white_to_move else -1
        if self.board[row-d][col] == '--':
            moves.append(Move((row, col), (row-d, col), self.board))
            if ((row == 6) if self.white_to_move else (row == 1)) and self.board[row-2*d][col] == '--':
                moves.append(Move((row, col), (row-2*d, col), self.board))
        if col-1 >= 0:
            if self.board[row-d][col-1][0] == ('b' if self.white_to_move else 'w'):
                moves.append(Move((row, col), (row-d, col-1), self.board))
        if col+1 <= 7:
            if self.board[row-d][col+1][0] == ('b' if self.white_to_move else 'w'):
                moves.append(Move((row, col), (row-d, col+1), self.board))
        return moves
    
    def get_knight_moves(self, row, col):
        moves = []
        dirs = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dir in dirs:
            if 0 <= row + dir[0] <= 7 and 0 <= col + dir[1] <= 7:
                if self.board[row + dir[0]][col + dir[1]][0] != ('w' if self.white_to_move else 'b'):
                    moves.append(Move((row, col), (row + dir[0], col + dir[1]), self.board))
        return moves
    def get_bishop_moves(self, row, col):
        moves =[]
        dirs = [-1, 1]
        for xd in dirs:
            for yd in dirs:
                clear = True
                steps = 1
                while clear:
                    cr, cc =  row+yd*steps, col+xd*steps
                    if not (0 <= cr <= 7 and 0 <= cc <= 7):
                        break
                    if self.board[cr][cc][0] == ('w' if self.white_to_move else 'b'):
                        break
                    if self.board[cr][cc][0] == ('b' if self.white_to_move else 'w'):
                        moves.append(Move((row, col), (cr, cc), self.board))
                        break
                    else:
                        moves.append(Move((row, col), (cr, cc), self.board))
                        steps += 1
        return moves
    def get_rook_moves(self, row, col):
        moves = []
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dir in dirs:
            clear = True
            steps = 1
            while clear:
                cr, cc =  row+dir[0]*steps, col+dir[1]*steps
                if not (0 <= cr <= 7 and 0 <= cc <= 7):
                    break
                if self.board[cr][cc][0] == ('w' if self.white_to_move else 'b'):
                    break
                if self.board[cr][cc][0] == ('b' if self.white_to_move else 'w'):
                    moves.append(Move((row, col), (cr, cc), self.board))
                    break
                else:
                    moves.append(Move((row, col), (cr, cc), self.board))
                    steps += 1
        return moves
    def get_queen_moves(self, row, col):
        moves = []
        moves += self.get_rook_moves(row, col)
        moves += self.get_bishop_moves(row, col)
        return moves
    def get_king_moves(self, row, col):
        moves = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == y == 0 or not (0 <= row+y <= 7 and 0 <= col+x <= 7):
                    continue
                if (self.board[row+y][col+x][0] == ('w' if self.white_to_move else 'b')):
                    continue
                moves.append(Move((row, col), (row+y, col+x), self.board))
        return moves
    


class Move:
    def __init__(self, start_square, end_square, board, special_move=False):
        self.start_square = start_square
        self.start_row = self.start_square[0]
        self.start_col = self.start_square[1]
        self.end_square = end_square
        self.end_row = self.end_square[0]
        self.end_col = self.end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_castle = False
        self.is_promotion = False
        self.is_enpassant = False
        match special_move:
            case 'castle':
                self.is_castle = True
            case 'promotion':
                self.is_promotion = True
            case 'enpassant':
                self.is_enpassant = True
        self.id = self.start_row + self.start_col*10 + self.end_row*100 + self.end_col*1000
    def __str__(self):
        col_to_alpha = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
        if self.piece_moved[1] == 'p':
            if self.piece_captured != '--':
                return col_to_alpha[self.start_col] + 'x' + col_to_alpha[self.end_col] + str(8-self.end_row)
            else:
                return col_to_alpha[self.end_col] + str(8-self.end_row)
        elif self.piece_moved[1] == 'n':
            if self.piece_captured != '--':
                return 'N' + 'x' + col_to_alpha[self.end_col] + str(8-self.end_row)
            else:
                return 'N' + col_to_alpha[self.end_col] + str(8-self.end_row)
        elif self.piece_moved[1] == 'b':
            if self.piece_captured != '--':
                return 'B' + 'x' + col_to_alpha[self.end_col] + str(8-self.end_row)
            else:
                return 'B' + col_to_alpha[self.end_col] + str(8-self.end_row)
        elif self.piece_moved[1] == 'r':
            if self.piece_captured != '--':
                return 'R' + 'x' + col_to_alpha[self.end_col] + str(8-self.end_row)
            else:
                return 'R' + col_to_alpha[self.end_col] + str(8-self.end_row)
        elif self.piece_moved[1] == 'q':
            if self.piece_captured != '--':
                return 'Q' + 'x' + col_to_alpha[self.end_col] + str(8-self.end_row)
            else:
                return 'Q' + col_to_alpha[self.end_col] + str(8-self.end_row)
        elif self.piece_moved[1] == 'k':
            if self.piece_captured != '--':
                return 'K' + 'x' + col_to_alpha[self.end_col] + str(8-self.end_row)
            else:
                return 'K' + col_to_alpha[self.end_col] + str(8-self.end_row)
        return 'placeholder'
    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return self.id == other.id
    