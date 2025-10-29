import pygame
import sys
import constants as const
from controller import GameController
from view import GameView
from player import HumanPlayer, AIPlayer

class Application:
    """
    The main application class that runs the game loop,
    handles events, and coordinates the controller and view.
    """
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
        pygame.display.set_caption("Othello (Reversi) - OOP")
        self.clock = pygame.time.Clock()
        
        self.game_state = "INTRO" # "INTRO", "PLAYING", "GAME_OVER"
        self.game_controller = None
        
        # Define button rects
        btn_width = 200
        btn_height = 60
        self.start_btn_rect = pygame.Rect(
            (const.WIDTH // 2) - (btn_width // 2), 
            const.HEIGHT - 150, 
            btn_width, 
            btn_height
        )
        self.reset_btn_rect = pygame.Rect(
            (const.WIDTH // 2) - (btn_width // 2), 
            const.HEIGHT - 100, 
            btn_width, 
            btn_height
        )
        
        # Timer for AI "thinking" delay
        self.ai_think_timer = 0
        self.ai_think_delay = 1000 # 1 second in milliseconds

    def run(self):
        """The main game loop."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(60) # Limit to 60 FPS

    def handle_events(self):
        """Handles all user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        """Delegates mouse clicks based on the game state."""
        
        if self.game_state == "INTRO":
            if self.start_btn_rect.collidepoint(pos):
                self.game_controller = GameController(ai_difficulty=4)
                self.game_state = "PLAYING"
        
        elif self.game_state == "PLAYING":
            # Only process clicks if it's the human's turn
            if isinstance(self.game_controller.current_player, HumanPlayer):
                clicked_row = pos[1] // const.SQUARE_SIZE
                clicked_col = pos[0] // const.SQUARE_SIZE
                self.game_controller.make_human_move(clicked_row, clicked_col)
        
        elif self.game_state == "GAME_OVER":
            if self.reset_btn_rect.collidepoint(pos):
                self.game_controller = GameController(ai_difficulty=4)
                self.game_state = "PLAYING"

    def update(self):
        """Updates the game logic."""
        if self.game_state == "PLAYING":
            # Check if game ended
            if self.game_controller.game_over:
                self.game_state = "GAME_OVER"
                return

            # Handle AI's turn
            if isinstance(self.game_controller.current_player, AIPlayer):
                # Start or continue the "thinking" timer
                if self.ai_think_timer == 0:
                    self.ai_think_timer = pygame.time.get_ticks()
                    pygame.display.set_caption("Othello (Reversi) - AI is thinking...")
                
                # Check if the delay has passed
                if pygame.time.get_ticks() - self.ai_think_timer >= self.ai_think_delay:
                    self.game_controller.run_ai_turn()
                    self.ai_think_timer = 0 # Reset timer
                    pygame.display.set_caption("Othello (Reversi) - OOP")


    def draw(self):
        """Draws the correct screen based on the game state."""
        
        if self.game_state == "INTRO":
            GameView.draw_intro_screen(self.screen, self.start_btn_rect)
        
        elif self.game_state == "PLAYING":
            GameView.draw_board(self.screen)
            # Pass the raw 8x8 grid from the board object
            GameView.draw_pieces(self.screen, self.game_controller.board.board)
            
            # Show valid moves only for the human
            if isinstance(self.game_controller.current_player, HumanPlayer):
                GameView.draw_valid_moves(self.screen, self.game_controller.valid_moves)
        
        elif self.game_state == "GAME_OVER":
            # Get scores from the controller's board
            black_score, white_score = self.game_controller.board.count_pieces()
            GameView.draw_game_over_screen(self.screen, black_score, white_score, self.reset_btn_rect)

# --- Entry Point ---
if __name__ == "__main__":
    app = Application()
    app.run()

