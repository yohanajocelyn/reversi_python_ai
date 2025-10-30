import pygame
import sys
import constants as const
from game_logic import GameLogic
from aiplayer import AIPlayer
from game_ui import GameUI

class Game:
    
    @staticmethod
    def run_game():
        # Initialize all Pygame modules
        pygame.init()
        
        # Set up the game window
        screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
        pygame.display.set_caption("Othello (Reversi)")
        
        # Set up the game clock to control FPS
        clock = pygame.time.Clock()

        # Add game state to handle the intro screen, playign screen, and game over screen
        game_state = "INTRO"

        # --- Define Players ---
        # Human will be Black, AI will be White
        HUMAN_PLAYER = const.BLACK_PIECE
        AI_PLAYER = const.WHITE_PIECE

        # Initialize the game objects as empty first because hrs melalui screen intro dulu
        ai = None
        game = None
        valid_moves = []

        # SET BTN2 UNTUK SCREEN INTRO DAN GAMEOVER
        btn_width = 200
        btn_height = 60

        # Start button
        start_btn_rect = pygame.Rect(
            (const.WIDTH // 2) - (btn_width // 2), 
            const.HEIGHT - 150, 
            btn_width, 
            btn_height
        )

        # Reset buttonnya
        reset_btn_rect = pygame.Rect(
            (const.WIDTH // 2) - (btn_width // 2), 
            const.HEIGHT - 100, 
            btn_width, 
            btn_height
        )

        running = True
        while running:
            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if game_state == "INTRO":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if start_btn_rect.collidepoint(event.pos):
                            game_state = "PLAYING"
                            # Sekarang baru bikin objek-objek gamenya
                            # --- Create an instance of the game logic ---
                            game = GameLogic()
                            ai = AIPlayer(AI_PLAYER)
                            valid_moves = game.get_valid_moves()

                elif game_state == "PLAYING":
                    if event.type == pygame.MOUSEBUTTONDOWN and game.current_player == HUMAN_PLAYER:
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
                                print(f"Player {game.current_player} (AI) has no moves! Skipping turn.")
                                game.switch_player()
                                valid_moves = game.get_valid_moves()
                                
                                # If *still* no moves, the game is over
                                if not valid_moves:
                                    print("Game Over! No players have valid moves.")
                                    game_state = "GAME_OVER"
                
                elif game_state == "GAME_OVER":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Check if kita click di reset buttonnya
                        if reset_btn_rect.collidepoint(event.pos):
                            # Reset game => Sama kek mulai game baru tadi
                            game = GameLogic()
                            ai = AIPlayer(AI_PLAYER)
                            valid_moves = game.get_valid_moves()
                            game_state = "PLAYING"
            
            # Game Logic dan Drawing (based on the states)
            if game_state == "INTRO":
                GameUI.draw_intro_screen(screen, start_btn_rect)
            elif game_state == "PLAYING":
                # (We do this here so the player sees the board *before* the AI thinks)
                GameUI.draw_board(screen)
                GameUI.draw_pieces(screen, game.board)

            # --- AI's Turn (No event checking needed) ---
                if game.current_player == AI_PLAYER:
                    pygame.display.flip() # Show the board

                    pygame.time.wait(1000)
                    
                    # --- Get the AI's move ---
                    pygame.display.set_caption("Othello (Reversi) - AI is thinking...")
                    best_move = ai.find_best_move(game)
                    pygame.display.set_caption("Othello (Reversi)")

                    if best_move:
                        # --- Make the AI's move ---
                        game.make_move(best_move[0], best_move[1])
                        
                        # --- Get valid moves for the *next* player (Human) ---
                        valid_moves = game.get_valid_moves()

                        # --- Handle skipped turn (if Human has no moves) ---
                        if not valid_moves:
                            print(f"Player {game.current_player} (Human) has no moves! Skipping turn.")
                            game.switch_player()
                            valid_moves = game.get_valid_moves() # Get moves for AI again
                            
                            # If *still* no moves, game is over
                            if not valid_moves:
                                print("Game Over! No players have valid moves.")
                                game_state = "GAME_OVER"
                    else:
                        # This case handles if the AI *starts* its turn but has no moves
                        # (which should be caught by the human's turn logic, but this is safe)
                        print(f"Player {game.current_player} (AI) has no moves! Skipping turn.")
                        game.switch_player()
                        valid_moves = game.get_valid_moves() # Get moves for Human
                        if not valid_moves:
                            print("Game Over! No players have valid moves.")
                            game_state = "GAME_OVER"

                if game.current_player == HUMAN_PLAYER:
                    GameUI.draw_valid_moves(screen, valid_moves)

            elif game_state == "GAME_OVER":
                GameUI.draw_game_over_screen(screen, game, reset_btn_rect)

            # --- Update Display ---
            pygame.display.flip()
            
            # --- Frame Limiting ---
            clock.tick(60)

        # --- Shutdown ---
        pygame.quit()

        sys.exit()