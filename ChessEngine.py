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

        self.move_functions = {
            "p": self.get_pawn_moves,
            "n": self.get_knight_moves,
            "b": self.get_bishop_moves,
            "r": self.get_rook_moves,
            "q": self.get_queen_moves,
            "k": self.get_king_moves,
        }

        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.can_castle = {'wk':True, 'wq':True, 'bk':True, 'bq':True}

    def make_move(self, move):
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.board[move.start_row][move.start_col] = '--'
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.is_castle:
            match move.is_castle:
                case 'wk':
                    self.make_move(Move((7, 7), (7, 5), self.board))
        if move.piece_moved == 'wk':
            self.white_king_location = (move.end_row, move.end_col)
            self.can_castle['wk'] = False
            self.can_castle['wq'] = False
        elif move.piece_moved == 'bk':
            self.black_king_location = (move.end_row, move.end_col)
            self.can_castle['bk'] = False
            self.can_castle['bq'] = False
        print(self.can_castle)
        print(self.white_king_location)

    def undo_move(self):
        if len(self.move_log) <= 0:
            return
        move = self.move_log.pop()
        self.board[move.end_row][move.end_col] = move.piece_captured
        self.board[move.start_row][move.start_col] = move.piece_moved
        self.white_to_move = not self.white_to_move
        if move.piece_moved == 'wk':
            self.white_king_location = (move.start_row, move.start_col)
        elif move.piece_moved == 'bk':
            self.black_king_location = (move.start_row, move.start_col)

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves)
        return moves

    def get_valid_moves(self):
        moves = self.get_all_possible_moves()
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return moves
    
    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location)
        else:
            return self.square_under_attack(self.black_king_location)

    def square_under_attack(self, square):
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opp_moves:
            if move.end_row == square[0] and move.end_col == square[1]:
                return True
        return False
    
    def get_pawn_moves(self, row, col, moves):
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

    def get_knight_moves(self, row, col, moves):
        dirs = [-2, -1, 1, 2]
        for x in dirs:
            for y in dirs:
                if abs(x) == abs(y) or  not (0 <= row + y <= 7 and 0 <= col + x <= 7):
                    continue
                if self.board[row+y][col+x][0] == ('w' if self.white_to_move else 'b'):
                    continue
                else:
                    moves.append(Move((row, col), (row+y, col+x), self.board))
        return moves
    
    def get_bishop_moves(self, row, col, moves):
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

    def get_rook_moves(self, row, col, moves):
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

    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)
        return moves

    def get_king_moves(self, row, col, moves):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == y == 0 or not (0 <= row+y <= 7 and 0 <= col+x <= 7):
                    continue
                if (self.board[row+y][col+x][0] == ('w' if self.white_to_move else 'b')):
                    continue
                moves.append(Move((row, col), (row+y, col+x), self.board))
        if self.white_to_move:
            if self.can_castle['wk'] and \
                self.board[self.white_king_location[0]][self.white_king_location[1]+1] == '--' and \
                self.board[self.white_king_location[0]][self.white_king_location[1]+2] == '--':
                moves.append(Move((row, col), (row, col+2), self.board, is_castle='wk'))
        return moves
                
                

class Move:
    def __init__(self, start_square, end_square, board, is_castle=''):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        self.is_castle = is_castle

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return self.moveID == other.moveID


    def __str__(self):
        return self.getRankFile(self.start_row, self.start_col) + ' ' + self.getRankFile(self.end_row, self.end_col)
    
    def getRankFile(self, row, col):
        file_to_col = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        col_to_file = {v:k for k, v in file_to_col.items()}
        return col_to_file[col] + str(8-row)