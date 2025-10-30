# --- Constants ---
# Dimensi dari papannya
# Ini semua sebagai konstanta yang bisa dipakai di file UI nanti
ROWS = 8
COLS = 8
SQUARE_SIZE = 80 # Ukuran dari tiap kotak pada papannya, dalam pixel

# Total window dimensions
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE

# Representasi dari kondisi suatu kotak, kalau kosong (gaada disk) = 0, dstnya sesuai di bawah ini
EMPTY = 0
BLACK_PIECE = 1
WHITE_PIECE = 2

# Setting warna dari papan, garis, intinya setting warna dari komponen-komponen UI gamenya
BOARD_COLOR = (0, 128, 0)      # "Felt green"
LINE_COLOR = (0, 0, 0)         # Black grid lines
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VALID_MOVE_COLOR = (255, 255, 0) # Yellow for the hint dots

# Ukuran dari titik hint valid moves untuk manusianya
PIECE_RADIUS = SQUARE_SIZE // 2 - 5
HINT_RADIUS = SQUARE_SIZE // 6