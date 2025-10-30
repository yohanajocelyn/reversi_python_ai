import constants as const

# --- Game "Brains" Class ---
# Class ini hanya mengatur semua aturan, status papan, dan membuat move-move
# Tidak mengurus pembuatan UI sama sekali
class GameLogic:
    # Constructor dari class GameLogic
    def __init__(self):
        self.board = self.create_board()
        self.current_player = const.BLACK_PIECE # Seperti rule di intro screen, player (human) selalu berwarna hitam dan main duluan

    # def untuk set initial state yaitu papan yang kosong tetapi 4 kotak di tengah diisi dengan hitam dan putih (memang initial state dari game REVERSI)
    def create_board(self):
        # Initializes the 8x8 board grid and places the four starting pieces
        board = [[const.EMPTY] * const.COLS for _ in range(const.ROWS)]
        # Place the four starting pieces
        board[3][3] = const.WHITE_PIECE
        board[3][4] = const.BLACK_PIECE
        board[4][3] = const.BLACK_PIECE
        board[4][4] = const.WHITE_PIECE
        return board

    # def yang mengatur pergantian player (antara human dan "ai"nya)
    def switch_player(self):
        # Swaps the current player.
        self.current_player = const.WHITE_PIECE if self.current_player == const.BLACK_PIECE else const.BLACK_PIECE

    # def untuk melihat dan mendapatkan tempat-tempat yang valid untuk move selanjutnya
    def get_valid_moves(self):
        # Generates a list of all valid (row, col) moves for the current player.
        valid_moves = []
        for r in range(const.ROWS):
            for c in range(const.COLS):
                if self.is_valid_move(r, c):
                    valid_moves.append((r, c))
        return valid_moves

    # Bagian dari function di atasnya, dia yang ngecek apakah sebuah kotak itu valid move untuk sang player yang lagi main sekarang
    # Sesuai aturan REVERSI, move valid kalau kotak itu kosong dan bisa "outflank" minimal 1 piece lawan di salah satu dari 8 arah
    # Kalau gk memenuhi syarat itu, gk dianggap sebagai valid move
    def is_valid_move(self, row, col):
        if self.board[row][col] != const.EMPTY:
            return False

        opponent = const.WHITE_PIECE if self.current_player == const.BLACK_PIECE else const.BLACK_PIECE

        # Check dari 8 arah secara horizontal, vertical, diagonal
        # (dr, dc) is the "direction vector" -> (delta_row, delta_col)
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            r, c = row + dr, col + dc
            
            # This flag tracks if we've found at least one opponent piece
            # in this direction before finding our own.
            found_opponent = False

            # Keep moving in this direction
            while 0 <= r < const.ROWS and 0 <= c < const.COLS:
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

        opponent = const.WHITE_PIECE if self.current_player == const.BLACK_PIECE else const.BLACK_PIECE
        pieces_to_flip = []

        # 1. Find all pieces to flip
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            r, c = row + dr, col + dc
            potential_flips_in_this_direction = []

            while 0 <= r < const.ROWS and 0 <= c < const.COLS:
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
