import constants as const

class Board:
    """
    Manages the 8x8 grid and the rules for placing pieces.
    It does not know whose turn it is, only the rules for a given player.
    """
    
    def __init__(self):
        """
        Initializes the board by creating the 8x8 grid.
        """
        self.board = self.create_board()

    def create_board(self):
        """
        Sets up the empty 8x8 grid and places the four 
        starting pieces in the center.
        """
        board = [[const.EMPTY] * const.COLS for _ in range(const.ROWS)]
        # Place the four starting pieces
        board[3][3] = const.WHITE_PIECE
        board[3][4] = const.BLACK_PIECE
        board[4][3] = const.BLACK_PIECE
        board[4][4] = const.WHITE_PIECE
        return board

    def get_piece(self, row, col):
        """
        A helper method to get the piece at a specific (row, col).
        """
        return self.board[row][col]

    def is_on_board(self, r, c):
        """
        A helper to check if a (r, c) coordinate is on the 8x8 grid.
        """
        return 0 <= r < const.ROWS and 0 <= c < const.COLS
    
    def get_pieces_to_flip(self, row, col, player_piece):
        """
        Finds all opponent pieces that would be flipped by placing
        a piece at (row, col) for player_piece.
        Returns a list of (r, c) tuples.
        """
        opponent_piece = const.WHITE_PIECE if player_piece == const.BLACK_PIECE else const.BLACK_PIECE
        pieces_to_flip = []

        # Check all 8 directions
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            r, c = row + dr, col + dc
            potential_flips_in_this_direction = []

            while self.is_on_board(r, c):
                if self.board[r][c] == opponent_piece:
                    potential_flips_in_this_direction.append((r, c))
                elif self.board[r][c] == player_piece:
                    pieces_to_flip.extend(potential_flips_in_this_direction)
                    break
                else: # Hit an empty square
                    break
                r += dr
                c += dc
        
        return pieces_to_flip

    def is_valid_move(self, row, col, player_piece):
        """
        Checks if a move is valid for a specific player.
        A move is valid if the square is empty and it flips at least one
        opponent piece.
        """
        if not self.is_on_board(row, col) or self.board[row][col] != const.EMPTY:
            return False
        
        return len(self.get_pieces_to_flip(row, col, player_piece)) > 0

    def get_all_valid_moves(self, player_piece):
        """
        Generates a list of all (row, col) valid moves for the given player.
        """
        valid_moves = []
        for r in range(const.ROWS):
            for c in range(const.COLS):
                if self.is_valid_move(r, c, player_piece):
                    valid_moves.append((r, c))
        return valid_moves

    def apply_move(self, row, col, player_piece):
        """
        Places a piece on the board at (row, col) and flips all
        outflanked opponent pieces.
        (Assumes the move has already been validated).
        """
        pieces_to_flip = self.get_pieces_to_flip(row, col, player_piece)
        
        self.board[row][col] = player_piece

        for r_flip, c_flip in pieces_to_flip:
            self.board[r_flip][c_flip] = player_piece
            
    def count_pieces(self):
        """
        Counts the number of black and white pieces on the board.
        Returns: (int, int): A tuple of (black_score, white_score)
        """
        black_score = 0
        white_score = 0
        for r in range(const.ROWS):
            for c in range(const.COLS):
                if self.board[r][c] == const.BLACK_PIECE:
                    black_score += 1
                elif self.board[r][c] == const.WHITE_PIECE:
                    white_score += 1
        return black_score, white_score