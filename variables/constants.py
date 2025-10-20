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