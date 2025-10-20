import pygame
import sys
from variables import constants as const
from game.game_logic import GameLogic
from ui.game_ui import GameUI

class Game:
    def run_game(self):
        # Initialize all Pygame modules
        pygame.init()
        
        # Set up the game window
        screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
        pygame.display.set_caption("Othello (Reversi)")
        
        # Set up the game clock to control FPS
        clock = pygame.time.Clock()
        
        # --- Create an instance of the game logic ---
        game = GameLogic()
        
        # --- Get the first set of valid moves ---
        valid_moves = game.get_valid_moves()

        running = True
        while running:
            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # 1. Get mouse position in pixels
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # 2. Convert pixel coordinates to board (row, col)
                    clicked_row = mouse_y // const.SQUARE_SIZE
                    clicked_col = mouse_x // const.SQUARE_SIZE
                    
                    # 3. Check if the clicked square is in our list of valid moves
                    if (clicked_row, clicked_col) in valid_moves:
                        
                        # --- Make the move ---
                        game.make_move(clicked_row, clicked_col)
                        
                        # --- Get the valid moves for the *next* player ---
                        valid_moves = game.get_valid_moves()
                        
                        # --- Handle a skipped turn ---
                        # If the new player has no valid moves, skip their turn
                        if not valid_moves:
                            print(f"Player {game.current_player} has no moves! Skipping turn.")
                            game.switch_player()
                            valid_moves = game.get_valid_moves()
                            
                            # If *still* no moves, the game is over
                            if not valid_moves:
                                print("Game Over! No players have valid moves.")
                                running = False # End the game

            gameUi = GameUI()

            # --- Drawing ---
            # 1. Draw the static board (background and grid)
            gameUi.draw_board(screen)
            
            # 2. Draw the pieces on top of the board (using the logic's board)
            gameUi.draw_pieces(screen, game.board)

            # 3. NEW: Draw the hint dots for valid moves
            gameUi.draw_valid_moves(screen, valid_moves)

            # --- Update Display ---
            pygame.display.flip()
            
            # --- Frame Limiting ---
            clock.tick(60)

        # --- Shutdown ---
        pygame.quit()
        sys.exit()