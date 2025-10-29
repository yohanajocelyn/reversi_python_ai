import math
import copy
import constants as const
# We will import controller.py, but to avoid circular import, we use type hinting
# This tells python "a 'GameController' object will be passed here"
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller import GameController

# --- Player Base Class ---
class Player:
    """Base class for all players."""
    def __init__(self, piece_color):
        self.piece = piece_color
        self.opponent_piece = const.WHITE_PIECE if piece_color == const.BLACK_PIECE else const.BLACK_PIECE

    def get_move(self, game_controller: 'GameController'):
        """
        Abstract method to get a move.
        'game_controller' is an instance of the main Game controller class.
        """
        raise NotImplementedError

# --- Human Player ---
class HumanPlayer(Player):
    """A player controlled by human mouse clicks."""
    def __init__(self, piece_color):
        super().__init__(piece_color)

    def get_move(self, game_controller: 'GameController'):
        # For a human, move selection is handled by the main.py event loop.
        # This method won't actually be called.
        pass

# --- AI Player ---
class AIPlayer(Player):
    """
    A player controlled by the Minimax algorithm.
    This is your existing AIPlayer class, refactored to inherit from Player.
    """
    def __init__(self, piece_color, difficulty_depth=4):
        super().__init__(piece_color)
        self.depth = difficulty_depth
        # Heuristic positional weights
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

    def get_move(self, game_controller: 'GameController'):
        """
        This function replaces your 'find_best_move'.
        It takes the main GameController object as state.
        """
        # Get valid moves for *itself* from the controller's board
        valid_moves = game_controller.board.get_all_valid_moves(self.piece)
        
        if not valid_moves:
            return None

        best_move = None
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf

        for move in valid_moves:
            # Simulate by creating a deepcopy of the *game_controller*
            simulated_game = copy.deepcopy(game_controller)
            
            # Use the controller's logic to make a move (this updates its state)
            simulated_game.board.apply_move(move[0], move[1], self.piece)
            simulated_game.update_after_move() # This handles player switching, etc.
            
            # Pass the new game state to alpha_beta
            # It's now the minimizing player's turn
            move_score = self.alpha_beta(simulated_game, self.depth - 1, alpha, beta, False) 

            if move_score > best_score:
                best_score = move_score
                best_move = move
            alpha = max(alpha, best_score)
            
        print(f"AI chose move: {best_move} with score: {best_score}")
        return best_move

    def evaluate_board(self, board, game_over):
        """
        Evaluates the board state.
        'board' is an instance of your Board class.
        """
        if game_over:
            black_score, white_score = board.count_pieces()
            if self.piece == const.BLACK_PIECE:
                ai_score, opp_score = black_score, white_score
            else:
                ai_score, opp_score = white_score, black_score
            
            if ai_score > opp_score: return math.inf
            elif opp_score > ai_score: return -math.inf
            else: return 0
        
        # Heuristic for a game in progress
        ai_total_weight = 0
        opp_total_weight = 0
        
        for r in range(const.ROWS):
            for c in range(const.COLS):
                weight = self.POSITIONAL_WEIGHTS[r][c]
                piece = board.get_piece(r, c)
                if piece == self.piece:
                    ai_total_weight += weight
                elif piece == self.opponent_piece:
                    opp_total_weight += weight
        return ai_total_weight - opp_total_weight

    def alpha_beta(self, game_state: 'GameController', depth, alpha, beta, is_maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning.
        'game_state' is a GameController object.
        """
        
        # Check if the game is over in this simulated state
        if game_state.game_over:
            return self.evaluate_board(game_state.board, game_over=True)

        # Check if max depth is reached
        if depth == 0:
            return self.evaluate_board(game_state.board, game_over=False)

        # The valid moves are for the player whose turn it *currently* is
        # in the simulated game_state
        valid_moves = game_state.valid_moves

        # Note: The game_state's update_after_move logic already handles skipped turns,
        # so we just need to check if valid_moves is empty.
        if not valid_moves:
             # This should be caught by game_over, but as a safeguard:
            return self.evaluate_board(game_state.board, game_over=False)


        if is_maximizing_player:
            best_value = -math.inf
            for move in valid_moves:
                new_game_state = copy.deepcopy(game_state)
                new_game_state.board.apply_move(move[0], move[1], new_game_state.current_player.piece)
                new_game_state.update_after_move()
                
                value = self.alpha_beta(new_game_state, depth - 1, alpha, beta, False)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
            return best_value
            
        else: # Minimizing player
            best_value = math.inf
            for move in valid_moves:
                new_game_state = copy.deepcopy(game_state)
                new_game_state.board.apply_move(move[0], move[1], new_game_state.current_player.piece)
                new_game_state.update_after_move()
                
                value = self.alpha_beta(new_game_state, depth - 1, alpha, beta, True)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if alpha >= beta:
                    break
            return best_value