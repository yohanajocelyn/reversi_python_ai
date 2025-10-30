# --- Constants ---
import copy
# Diperlukan karena cara kerja algoritma MiniMax adalah AInya akan mencoba untuk melihat simulasi game dari move-move lain, jadi perlu
# pakai copy.deepcopy untuk membuat salinan independen (cuman buat simulasi) dari state game saat ini

import math
# Buat bisa pakai value inf dan -inf di alpha beta pruning optimization dari MiniMax Algorithm

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

# --- Game "Brains" Class ---
# Class ini hanya mengatur semua aturan, status papan, dan membuat move-move
# Tidak mengurus pembuatan UI sama sekali
class GameLogic:
    # Constructor dari class GameLogic
    def __init__(self):
        self.board = self.create_board()
        self.current_player = BLACK_PIECE # Seperti rule di intro screen, player (human) selalu berwarna hitam dan main duluan

    # def untuk set initial state yaitu papan yang kosong tetapi 4 kotak di tengah diisi dengan hitam dan putih (memang initial state dari game REVERSI)
    def create_board(self):
        # Initializes the 8x8 board grid and places the four starting pieces
        board = [[EMPTY] * COLS for _ in range(ROWS)]
        # Place the four starting pieces
        board[3][3] = WHITE_PIECE
        board[3][4] = BLACK_PIECE
        board[4][3] = BLACK_PIECE
        board[4][4] = WHITE_PIECE
        return board

    # def yang mengatur pergantian player (antara human dan "ai"nya)
    def switch_player(self):
        # Swaps the current player.
        self.current_player = WHITE_PIECE if self.current_player == BLACK_PIECE else BLACK_PIECE

    # def untuk melihat dan mendapatkan tempat-tempat yang valid untuk move selanjutnya
    def get_valid_moves(self):
        # Generates a list of all valid (row, col) moves for the current player.
        valid_moves = []
        for r in range(ROWS):
            for c in range(COLS):
                if self.is_valid_move(r, c):
                    valid_moves.append((r, c))
        return valid_moves

    # Bagian dari function di atasnya, dia yang ngecek apakah sebuah kotak itu valid move untuk sang player yang lagi main sekarang
    # Sesuai aturan REVERSI, move valid kalau kotak itu kosong dan bisa "outflank" minimal 1 piece lawan di salah satu dari 8 arah
    # Kalau gk memenuhi syarat itu, gk dianggap sebagai valid move
    def is_valid_move(self, row, col):
        if self.board[row][col] != EMPTY:
            return False

        opponent = WHITE_PIECE if self.current_player == BLACK_PIECE else BLACK_PIECE

        # Check dari 8 arah secara horizontal, vertical, diagonal
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

# Class dari AI nya
class AIPlayer:
    def __init__(self, player_piece, difficulty_depth=5):

        # Menyimpan apakah AI nya sedang main sebagai dirinya sendiri (putih) atau simulasi manusianya (hitam)
        self.player_piece = player_piece 
        self.opponent_piece = WHITE_PIECE if player_piece == BLACK_PIECE else BLACK_PIECE

        # Difficulty depth ini adalah tingkat kedalaman tree MiniMaxnya yang akan dilihat AInya / seberapa jauh dia berusaha melihat kemungkinan masa depannya
        # Defaultnya 12 kalau tidak diset di run_game
        self.depth = difficulty_depth

        # Bobot dari peletakan posisi
        # Ini adalah bagian "heuristic" dari AInya
        # Heuristic = a rule or piece of information used in or enabling problem-solving or decision-making
        # Pojokkan paling tinggi karena dia bisa outflank dari 3 posisi
        # Kotak di sebelah pojokkan valuenya turun karena bisa di-outflank
        # Kotak ujung-ujung lainnya masih lebih mending

        self.POSITIONAL_WEIGHTS = [
            [120, -20, 20,  5,  5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20,  5,  5, 20, -20, 120]
        ]

    # Function untuk evaluaasi nilai papan saat ini berdasarkan bobot heuristic di atas
    # Function yang return nilai dari sebuah leaf node di tree MiniMaxnya
    # Apakah sebuah move akan menghasilkan nilai bobot berapa untuk si AI dan nilai bobot berapa untuk manusianya
    # Nilai positif = bagus untuk AInya, nilai negatif = semakin bagus untuk manusianya
    def evaluate_board(self, board, game_over):

        # Kalau game over, scorenya adalah dari jumlah disk yang ada di papan untuk masing-masing player
        if game_over:
            ai_score = 0
            opp_score = 0
            for r in range(ROWS):
                for c in range(COLS):
                    if board[r][c] == self.player_piece:
                        ai_score += 1
                    elif board[r][c] == self.opponent_piece:
                        opp_score += 1
            
            # Ini untuk nilai absolut win dan lose
            if ai_score > opp_score:
                return math.inf  # AI wins
            elif opp_score > ai_score:
                return -math.inf # Human wins
            else:
                return 0 # Draw
        

        # --- Heuristic for a game in progress --- => Kalau bukan game over dan udh mencapai batas dari evaluasi depthnya (difficulty depth yang sudah diset tadi)
        # Hitung bobot untuk masing-masing player dari map heuristic di atas
        ai_total_weight = 0
        opp_total_weight = 0
        
        for r in range(ROWS):
            for c in range(COLS):
                weight = self.POSITIONAL_WEIGHTS[r][c]
                if board[r][c] == self.player_piece:
                    ai_total_weight += weight
                elif board[r][c] == self.opponent_piece:
                    opp_total_weight += weight

        # The score is the difference in positional weights
        return ai_total_weight - opp_total_weight


    # Function untuk mencari move dengan nilai bobot tertinggi
    def find_best_move(self, game_logic_instance):

        best_move = None # Variable yang akan menampung posisi kotak untuk move terbaik (r, c)
        best_score = -math.inf # Untuk AI yang mau maximize scorenya, dia menyimpan kemungkinan terburuk dulu
        alpha = -math.inf # Alpha adalah nilai terbaik yang Maximizer (AI) nya bisa jamin untuk sekarang
        beta = math.inf # Beta adalah nilai terbaik yang Minimizer (AI) nya bisa jamin untuk sekarang

        # Ambilkan semua valid move untuk AI nya saat ini
        valid_moves = game_logic_instance.get_valid_moves()

        # Looping untuk mencoba semua valid move yang bisa dilakukan si AI
        # Untuk setiap valid move yang bisa dilakukan AI nya sekarang, dia akan bikin tree of the possibilities pakai function alpha_beta
        for move in valid_moves:
            # Game nya di-deepcopy dulu untuk kepentingan simulasi saja, karena evaluasi MiniMaxnya tidak boleh mengubah state game yang asli
            simulated_game = copy.deepcopy(game_logic_instance)
            simulated_game.make_move(move[0], move[1])
            
            # Panggil function alpha_beta yang rekursif (bukan rekursif di sini, tapi rekursif di dalam dirinya sendiri nanti) -
            # - untuk mendapatkan score dari move yang sedang disimulasikan ini
            # depth - 1 karena kita sudah melakukan 1 move di level ini, jadi mengurangi difficulty depth yang bisa dia lakukan next
            # Diset False karena setelah AI (Maximizer) jalan, next manusianya yang jalan (Minimizer)
            move_score = self.alpha_beta(simulated_game, self.depth - 1, alpha, beta, False)

            # Untuk pertama, best_score pasti akan tergantikan oleh move_score karena best_score awalnya -inf
            if move_score > best_score:
                best_score = move_score
                best_move = move
            
            # Update alpha for the root node, the best score yang bisa AI nya jamin untuk dirinya sendiri saat ini
            alpha = max(alpha, best_score)
            
        # Log hasil pemikirannya
        print(f"AI chose move: {best_move} with score: {best_score}")
        return best_move

    # Function yang rekursif
    # game_state = Kondisi game saat ini (hasil deepcopy dari instance game_logic)
    # depth = Seberapa jauh AI nya boleh menerawang/melihat
    # alpha, beta = Variable yang dipakai untuk pruning
    # is_maximizing_player = Boolean untuk menandai apakah yang lagi dicek ini si AI atau manusianya
    def alpha_beta(self, game_state, depth, alpha, beta, is_maximizing_player):

        # Ambil semua valid move untuk player yang lagi dievaluasi sekarang
        valid_moves = game_state.get_valid_moves()
        
        # Cek kalau sudah tidak ada valid move untuk keduanya
        # Kalau keduanya sudah tidak ada valid move, kembalikan board evaluation sebagai game over
        if not valid_moves:
            temp_game = copy.deepcopy(game_state)
            temp_game.switch_player()
            if not temp_game.get_valid_moves():
                return self.evaluate_board(game_state.board, game_over=True)
            else:
                # Ini adalah kondisi kalau player yang lagi dievaluasi sekarang sudah tidak punya valid move
                # Tetap lanjutnya evaluasi MiniMax dari sudut pandang player lain
                # Kedalamannya tidak berkurang kareng ini dipaksa untuk diskip
                if is_maximizing_player:
                    # Kalau AI harus skip, jadi Min dicek
                    return self.alpha_beta(temp_game, depth, alpha, beta, False)
                else:
                    # Kalau manusia harus skip, evaluasi lanjut untuk Max/AI
                    return self.alpha_beta(temp_game, depth, alpha, beta, True)

        # Kalau sudah mencapai ujung kedalaman yang boleh dievaluasi, dia akan mengembalikan nilai evaluasi papan saat ini
        if depth == 0: # ****
            return self.evaluate_board(game_state.board, game_over=False)

        # Bagian yang rekursif
        if is_maximizing_player:
            best_value = -math.inf
            for move in valid_moves:
                # Simulasikan move yang bisa diambil pada copy-an dari game statenya
                new_game_state = copy.deepcopy(game_state)
                new_game_state.make_move(move[0], move[1])
                
                # Setelah Max jalan, next cek untuk Min
                value = self.alpha_beta(new_game_state, depth - 1, alpha, beta, False)
                # Kalau udh mentok nanti akan return positional weightnya di ****

                # Cek perbandingan antara best_value yang ditetapkan pertama dengan value yang baru didapat
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                
                # Bagian pruning dari loopnya, kalau manusia sudah punya nilai beta (skor terendah yang bisa dia jamin untuk dirinya sendiri) 
                # yang lebih kecil atau sama dengan alpha (skor tertinggi yang bisa AI jamin untuk dirinya sendiri)
                # Skip karena gamungkin si manusia (berdasarkan algoritma MiniMax) akan ambil move tersebut
                if alpha >= beta:
                    break # Beta cutoff
            return best_value
            
        else: # Minimizing player
            best_value = math.inf
            for move in valid_moves:
                # Simulate the move
                new_game_state = copy.deepcopy(game_state)
                new_game_state.make_move(move[0], move[1])
                
                # Recurse (it's now the maximizer's turn)
                value = self.alpha_beta(new_game_state, depth - 1, alpha, beta, True)
                
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                
                # Pruning
                if alpha >= beta:
                    break # Alpha cutoff
            return best_value