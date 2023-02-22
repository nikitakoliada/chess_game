
class GameState():
    def __init__(self):
        # Set up the initial board state
        self.board = [
            ['black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_bishop', 'black_knight', 'black_rook'],
            ['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn'],
            ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
            ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
            ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
            ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
            ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn'],
            ['white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight', 'white_rook'],
        ]

        self.white_move = True
        self.move_log = []
    
    def check_for_right_move(self, row, col):
        if self.check_for_empty(row, col) == True:
            return False
        if (self.white_move == True and "white" in self.board[row][col]) or (self.white_move == False and "black" in self.board[row][col]):
            return True

        

    def check_for_empty(self, row, col):
        if self.board[row][col] == 'empty':
            return True
        else:
            return False

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = 'empty'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_move = not self.white_move

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_capt
            self.white_move = not self.white_move
    def get_valid_moves(self):
        return self.get_pos_moves()

    def get_pos_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.check_for_right_move(r,c):
                    piece = self.board[r][c]
                    if "pawn" in piece:
                        self.get_pawn_moves(r, c, moves)
                    elif "rook" in piece:
                        self.get_rook_moves(r, c, moves)
                    elif "bishop" in piece:
                        self.get_bishop_moves(r, c, moves)
                    elif "knight" in piece:
                        self.get_pawn_moves(r, c, moves)
                    elif "queen" in piece:
                        self.get_queen_moves(r, c, moves)
                    elif "king" in piece:
                        self.get_king_moves(r, c, moves)

        return moves

    
    def get_pawn_moves(self, row, col, moves):
        color = "white" if self.white_move else "black"

        if self.white_move:
            if self.board[row-1][col] == 'empty':  # one ahead
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == 'empty': # two ahead
                    moves.append(Move((row, col), (row-2, col), self.board))
            #captures 
            if col-1 >= 0: 
                if self.board[row-1][col-1] != 'empty' and not color in self.board[row-1][col-1]:
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            if col+1 <= 7:
                if self.board[row-1][col+1] != 'empty' and not color in self.board[row-1][col+1]:
                    moves.append(Move((row, col), (row-1, col+1), self.board))
            
        else: # black move
            if self.board[row+1][col] == 'empty':  # one ahead
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == 'empty': # two ahead
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col-1 >= 0:
                if self.board[row+1][col-1] != 'empty' and not color in self.board[row+1][col-1]:
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            if col+1 <= 7:
                if self.board[row+1][col+1] != 'empty' and not color in self.board[row+1][col+1]:
                    moves.append(Move((row, col), (row+1, col+1), self.board))

    def get_rook_moves(self, row, col, moves):
       directions = ((-1, 0),(0, -1),( 1, 0),(0, 1))
       color = "white" if self.white_move else "black"
       for d in directions:
        for i in range(1, 8):
            r = row + d[0] * i
            c = col + d[1] * i
            if 8 > r >= 0 and 8 > c >= 0:
                square = self.board[r][c] 
                if square == "empty":
                     moves.append(Move((row, col), (r, c), self.board))
                elif not color in square:
                    moves.append(Move((row, col), (r, c), self.board))
                    break
                else:
                    break
            else: 
                break

    def get_bishop_moves(self, row, col, moves):
       directions = ((-1, -1),(1, -1),( -1, 1),(1, 1))
       color = "white" if self.white_move else "black"
       for d in directions:
        for i in range(1, 8):
            r = row + d[0] * i
            c = col + d[1] * i
            if 8 > r >= 0 and 8 > c >= 0:
                square = self.board[r][c] 
                if square == "empty":
                     moves.append(Move((row, col), (r, c), self.board))
                elif not color in square:
                    moves.append(Move((row, col), (r, c), self.board))
                    break
                else:
                    break
            else: 
                break
    
    def get_queen_moves(self, row, col, moves):
       self.get_bishop_moves(row, col, moves)
       self.get_rook_moves(row, col, moves)
       
    def get_king_moves(self, row, col, moves):
        directions = ((-1, -1),(1, -1),( -1, 1),(1, 1))
        color = "white" if self.white_move else "black"
        for d in directions:
            r = row + d[0]
            c = col + d[1]
            if 8 > r >= 0 and 8 > c >= 0:
                square = self.board[r][c] 
                if square == "empty":
                    moves.append(Move((row, col), (r, c), self.board))
                elif not color in square:
                    moves.append(Move((row, col), (r, c), self.board))
                    break
                else:    
                    break
            else: 
                break





class Move():
    #chess notation
    dig_to_rows = {"1" : 7, "2" : 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    character_to_col = {"a" : 0, "b" : 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}


    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_capt = board[self.end_row][self.end_col]

    def __eq__(self, other):
        if isinstance(other, Move):
            if self.start_row == other.start_row and self.start_col == other.start_col and self.end_col == other.end_col and self.end_row == other.end_row:
                return True
        return False
            
    def get_notation(self):
        return (self.start_row + self.start_col, self.end_row + self.end_col)

    def get_dig_char(self, row, col):
        return self.dig_to_rows.values().index(row) + self.character_to_col.values().index(col)



