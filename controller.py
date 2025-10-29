from board import Board
from player import HumanPlayer, AIPlayer
import constants as const

class GameController:
    """
    The main game controller. Manages the board, players,
    and game state (turns, game over).
    """
    
    def __init__(self, ai_difficulty=4):
        self.board = Board()
        self.player_black = HumanPlayer(const.BLACK_PIECE)
        self.player_white = AIPlayer(const.WHITE_PIECE, ai_difficulty)
        
        # Human (Black) always starts
        self.current_player = self.player_black 
        
        self.valid_moves = self.board.get_all_valid_moves(self.current_player.piece)
        self.game_over = False

    def switch_player(self):
        """Swaps the current player."""
        self.current_player = self.player_white if self.current_player == self.player_black else self.player_black

    def update_after_move(self):
        """
        Called after a move is applied. Switches player, gets new
        valid moves, and checks for skips or game over.
        """
        # 1. Switch to the next player
        self.switch_player()
        
        # 2. Get moves for the *new* player
        self.valid_moves = self.board.get_all_valid_moves(self.current_player.piece)
        
        # 3. Handle skipped turn
        if not self.valid_moves and not self.game_over:
            print(f"Player {self.current_player.piece} (Human) has no moves! Skipping turn.")
            self.switch_player() # Skip back
            self.valid_moves = self.board.get_all_valid_moves(self.current_player.piece)
            
            # 4. If *still* no moves, game is over
            if not self.valid_moves:
                print("Game Over! No players have valid moves.")
                self.game_over = True

    def make_human_move(self, row, col):
        """
        Attempts to make a move for the human player.
        Returns True if successful, False otherwise.
        """
        if (row, col) in self.valid_moves:
            # 1. Apply the move to the board
            self.board.apply_move(row, col, self.current_player.piece)
            # 2. Update game state (switch player, check skips, etc.)
            self.update_after_move()
            return True
        return False

    def run_ai_turn(self):
        """
        If the current player is an AI, get its move and make it.
        """
        if not self.game_over and isinstance(self.current_player, AIPlayer):
            # Pass *this entire game instance* to the AI
            move = self.current_player.get_move(self) 
            
            if move:
                self.board.apply_move(move[0], move[1], self.current_player.piece)
                self.update_after_move()
            else:
                # This case handles if AI *starts* its turn with no moves
                # (which should be caught by update_after_move, but is a good safeguard)
                print(f"AI has no moves! Skipping.")
                self.update_after_move()
