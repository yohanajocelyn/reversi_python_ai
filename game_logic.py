# --- Constants ---
import copy
import math

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

class AIPlayer:
    def __init__(self, player_piece, difficulty_depth=4):
        """
        Initializes the AI.
        :param player_piece: The piece the AI will play as (e.g., BLACK_PIECE or WHITE_PIECE)
        :param difficulty_depth: How many moves ahead the AI will look.
        """
        self.player_piece = player_piece
        self.opponent_piece = WHITE_PIECE if player_piece == BLACK_PIECE else BLACK_PIECE
        self.depth = difficulty_depth

        # Positional weights for the 8x8 board.
        # Corners are most valuable, edges are good, squares next to corners are bad.
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

    def evaluate_board(self, board, game_over):
        """
        Evaluates the current board state based on a heuristic.
        A positive score is good for the AI, negative is good for the Human.
        """
        
        # If the game is over, the score is based on the final piece count
        if game_over:
            ai_score = 0
            opp_score = 0
            for r in range(ROWS):
                for c in range(COLS):
                    if board[r][c] == self.player_piece:
                        ai_score += 1
                    elif board[r][c] == self.opponent_piece:
                        opp_score += 1
            
            if ai_score > opp_score:
                return math.inf  # AI wins
            elif opp_score > ai_score:
                return -math.inf # Human wins
            else:
                return 0 # Draw
        
        # --- Heuristic for a game in progress ---
        # We use positional weights, not just piece count
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


    def find_best_move(self, game_logic_instance):
        """
        This is the entry point for the AI.
        It iterates through all possible moves and finds the one with
        the highest score from the alpha_beta algorithm.
        """
        best_move = None
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf

        # Get all valid moves for the AI
        valid_moves = game_logic_instance.get_valid_moves()
        
        # (Optional) Shuffle moves to make the AI less predictable
        # random.shuffle(valid_moves) 

        for move in valid_moves:
            # Create a deep copy of the game state to simulate this move
            # We don't want to change the *actual* game board
            simulated_game = copy.deepcopy(game_logic_instance)
            simulated_game.make_move(move[0], move[1])
            
            # Call alpha_beta on the *resulting* board state
            # It's now the opponent's (minimizing) turn
            # We pass self.depth - 1 because one move has already been made
            move_score = self.alpha_beta(simulated_game, self.depth - 1, alpha, beta, False)

            # Update the best score and move
            if move_score > best_score:
                best_score = move_score
                best_move = move
            
            # Update alpha for the root node
            alpha = max(alpha, best_score)
            
        print(f"AI chose move: {best_move} with score: {best_score}")
        return best_move


    def alpha_beta(self, game_state, depth, alpha, beta, is_maximizing_player):
        """
        The core Minimax algorithm with Alpha-Beta Pruning.
        """
        
        # --- Check for Terminal/Base Cases ---
        valid_moves = game_state.get_valid_moves()
        
        # Check if the game is over (no moves for current player)
        if not valid_moves:
            # Check if the *other* player also has no moves (Game Over)
            temp_game = copy.deepcopy(game_state)
            temp_game.switch_player()
            if not temp_game.get_valid_moves():
                # Game is Over
                return self.evaluate_board(game_state.board, game_over=True)
            else:
                # This is a skipped turn, not a game-ending state
                # We must continue the search from the other player's perspective
                # The 'depth' doesn't decrease, as this is a forced "pass"
                if is_maximizing_player:
                    # AI (Max) has to skip, so Min plays
                    return self.alpha_beta(temp_game, depth, alpha, beta, False)
                else:
                    # Human (Min) has to skip, so Max plays
                    return self.alpha_beta(temp_game, depth, alpha, beta, True)

        # Base case: If we've reached the maximum depth, return the heuristic score
        if depth == 0:
            return self.evaluate_board(game_state.board, game_over=False)

        # --- Recursive Step ---
        if is_maximizing_player:
            best_value = -math.inf
            for move in valid_moves:
                # Simulate the move
                new_game_state = copy.deepcopy(game_state)
                new_game_state.make_move(move[0], move[1])
                
                # Recurse (it's now the minimizer's turn)
                value = self.alpha_beta(new_game_state, depth - 1, alpha, beta, False)
                
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                
                # Pruning
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