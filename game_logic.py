# --- Constants ---

# Board dimensions
ROWS = 8
COLS = 8
SQUARE_SIZE = 80 # Size of each square in pixels

# Total window dimensions
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE

# Piece representation (using numbers)
EMPTY = 0
BLACK_PIECE = 1
WHITE_PIECE = 2

# Colors (RGB)
BOARD_COLOR = (0, 128, 0)      # "Felt green"
LINE_COLOR = (0, 0, 0)         # Black grid lines
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VALID_MOVE_COLOR = (255, 255, 0) # Yellow for the hint dots

# Radius of pieces and hint dots
PIECE_RADIUS = SQUARE_SIZE // 2 - 5
HINT_RADIUS = SQUARE_SIZE // 6

# --- Game "Brains" Class ---
# This class handles all the rules, the board state, and making moves.
# It does NOT know about Pygame or drawing.
class GameLogic:
    def __init__(self):
        self.board = self.create_board()
        self.current_player = BLACK_PIECE

    def create_board(self):
        # Initializes the 8x8 board grid and places the four starting pieces.
        board = [[EMPTY] * COLS for _ in range(ROWS)]
        # Place the four starting pieces
        board[3][3] = WHITE_PIECE
        board[3][4] = BLACK_PIECE
        board[4][3] = BLACK_PIECE
        board[4][4] = WHITE_PIECE
        return board

    def switch_player(self):
        # Swaps the current player.
        self.current_player = WHITE_PIECE if self.current_player == BLACK_PIECE else BLACK_PIECE

    def get_valid_moves(self):
        # Generates a list of all valid (row, col) moves for the current player.
        valid_moves = []
        for r in range(ROWS):
            for c in range(COLS):
                if self.is_valid_move(r, c):
                    valid_moves.append((r, c))
        return valid_moves

    def is_valid_move(self, row, col):
        # 
        # Checks if placing a piece at (row, col) is a valid move.
        # A move is valid if:
        # 1. The square is empty.
        # 2. It outflanks at least one opponent piece in any of the 8 directions.
        # 
        # 1. If the square is not empty, it's not a valid move
        if self.board[row][col] != EMPTY:
            return False

        opponent = WHITE_PIECE if self.current_player == BLACK_PIECE else BLACK_PIECE

        # Check all 8 directions (horizontal, vertical, diagonal)
        # (dr, dc) is the "direction vector" -> (delta_row, delta_col)
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            r, c = row + dr, col + dc
            
            # This flag tracks if we've found at least one opponent piece
            # in this direction before finding our own.
            found_opponent = False

            # Keep moving in this direction
            while 0 <= r < ROWS and 0 <= c < COLS:
                if self.board[r][c] == opponent:
                    found_opponent = True
                elif self.board[r][c] == self.current_player:
                    # We found our own piece!
                    # If we found an opponent *before* this, it's a valid move.
                    if found_opponent:
                        return True
                    else:
                        # Found our own piece first, so this direction is invalid
                        break
                else: # self.board[r][c] == EMPTY
                    break # Ran into an empty square, invalid direction
                
                # Move to the next square in this direction
                r += dr
                c += dc
        
        # If we checked all 8 directions and none returned True, it's invalid
        return False

    def make_move(self, row, col):
        
        # Places a piece on the board at (row, col) and flips all
        # outflanked opponent pieces.
        # (Assumes the move is already validated)
        
        opponent = WHITE_PIECE if self.current_player == BLACK_PIECE else BLACK_PIECE
        pieces_to_flip = []

        # 1. Find all pieces to flip
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            r, c = row + dr, col + dc
            potential_flips_in_this_direction = []

            while 0 <= r < ROWS and 0 <= c < COLS:
                if self.board[r][c] == opponent:
                    # Found an opponent piece, add it to our *potential* list
                    potential_flips_in_this_direction.append((r, c))
                elif self.board[r][c] == self.current_player:
                    # Found our own piece, all potential flips are now *confirmed*
                    pieces_to_flip.extend(potential_flips_in_this_direction)
                    break
                else: # self.board[r][c] == EMPTY
                    # Ran into an empty square, clear potential flips for this direction
                    break
                
                r += dr
                c += dc
        
        # 2. Place the new piece
        self.board[row][col] = self.current_player

        # 3. Flip all the confirmed pieces
        for r_flip, c_flip in pieces_to_flip:
            self.board[r_flip][c_flip] = self.current_player
        
        # 4. Switch to the other player for the next turn
        self.switch_player()