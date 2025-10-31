import pygame
import sys
from game_logic import GameLogic, AIPlayer
import game_logic as const

# --- Game Drawing Class ---
# This class ONLY handles drawing to the screen.
# It uses "static methods" so we can call them without creating an instance.
class GameUI:
    WIDTH = const.WIDTH
    HEIGHT = const.HEIGHT

    @staticmethod
    def draw_intro_screen(screen, start_btn_rect, timer_buttons, minutes, seconds):

        text_color = (23, 42, 58)

        screen.fill((117, 221, 221))
        
        # Set fontsnya
        title_font = pygame.font.SysFont(None, 80, bold=True)
        subtitle_font = pygame.font.SysFont(None, 40, italic=True)
        rules_font = pygame.font.SysFont(None, 28)
        btn_font = pygame.font.SysFont(None, 42, bold=True)

        # Tambahan fitur timer
        timer_label_font = pygame.font.SysFont(None, 36, bold=True)
        timer_font = pygame.font.SysFont("monospace", 50, bold=True)
        timer_btn_font = pygame.font.SysFont(None, 50, bold=True)

        # Title Text
        title_text = title_font.render("REVERSI", True, text_color)
        title_rect = title_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 8))
        screen.blit(title_text, title_rect)

        # Subtitle text
        subtitle_text = subtitle_font.render("Human vas AI", True, text_color)
        subtitle_rect = subtitle_text.get_rect(center=(const.WIDTH // 2, title_rect.bottom + 30))
        screen.blit(subtitle_text, subtitle_rect)

        # Rules:
        rules = [
            "1. The human plays as the black disk and will go first.",
            "2. The goal is to have the most disks of your color at the end.",
            "3. A valid move must 'outflank' one or more opponent disks.",
            "4. Outflanked disks (horizontal, vertical, or diagonal)",
             " will be 'reversed'.",
            "5. A player without any valid moves will have their turn skipped."
        ]

        start_y = subtitle_rect.bottom + 40
        for i, rule in enumerate(rules):
            rule_text = rules_font.render(rule, True, text_color)
            rule_rect = rule_text.get_rect(center=(const.WIDTH // 2, start_y + i * 35))
            screen.blit(rule_text, rule_rect)

        # Bagian timer
        timer_position_y = start_y + (len(rules) * 30) + 40
        timer_label = timer_label_font.render("Set Game Timer", True, text_color)
        timer_label_rect = timer_label.get_rect(center=(const.WIDTH // 2, timer_position_y))
        screen.blit(timer_label, timer_label_rect)

        timer_str = f"{minutes:02}:{seconds:02}"
        timer_text = timer_font.render(timer_str, True, text_color)
        timer_rect = timer_text.get_rect(center=(const.WIDTH // 2, timer_position_y + 30))
        screen.blit(timer_text, timer_rect)

        for key, rect in timer_buttons.items():
            pygame.draw.rect(screen, text_color, rect, border_radius=8)
            if "up" in key:
                text = timer_btn_font.render("+", True, const.WHITE)
            else:
                text = timer_btn_font.render("-", True, const.WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        min_label = rules_font.render("Minutes", True, text_color)
        min_label_rect = min_label.get_rect(center=(timer_buttons["min_up"].centerx, timer_rect.bottom + 25))
        screen.blit(min_label, min_label_rect)
        sec_label = rules_font.render("Seconds", True, text_color)
        sec_label_rect = sec_label.get_rect(center=(timer_buttons["sec_up"].centerx, min_label_rect.bottom + 25))
        screen.blit(sec_label, sec_label_rect)
        
        # DRAW THE START BUTTON COMPONENT
        # Draw the rectangle shape of the button
        pygame.draw.rect(screen, text_color, start_btn_rect, border_radius=10)

        # Draw the text on the button
        btn_font = pygame.font.SysFont(None, 40)
        btn_text = btn_font.render("START", True, const.WHITE)
        btn_rect = btn_text.get_rect(center=start_btn_rect.center)
        screen.blit(btn_text, btn_rect)

    @staticmethod
    def draw_board(screen):
        # Draws the board background and grid line
        screen.fill(const.BOARD_COLOR)
        for i in range(const.ROWS + 1):
            pygame.draw.line(screen, const.LINE_COLOR, (0, i * const.SQUARE_SIZE), (const.WIDTH, i * const.SQUARE_SIZE), 2)
            pygame.draw.line(screen, const.LINE_COLOR, (i * const.SQUARE_SIZE, 0), (i * const.SQUARE_SIZE, const.BOARD_HEIGHT), 2)

    @staticmethod
    def draw_pieces(screen, board):
        # Draws all the pieces currently on the boar
        for row in range(const.ROWS):
            for col in range(const.COLS):
                piece = board[row][col]
                if piece != const.EMPTY:
                    color = const.BLACK if piece == const.BLACK_PIECE else const.WHITE
                    center_x = col * const.SQUARE_SIZE + const.SQUARE_SIZE // 2
                    center_y = row * const.SQUARE_SIZE + const.SQUARE_SIZE // 2
                    pygame.draw.circle(screen, color, (center_x, center_y), const.PIECE_RADIUS)

    @staticmethod
    def draw_valid_moves(screen, moves_list):
        
        # Draws hint dots for all valid moves.
        for row, col in moves_list:
            center_x = col * const.SQUARE_SIZE + const.SQUARE_SIZE // 2
            center_y = row * const.SQUARE_SIZE + const.SQUARE_SIZE // 2
            pygame.draw.circle(screen, const.VALID_MOVE_COLOR, (center_x, center_y), const.HINT_RADIUS)
    
    @staticmethod
    def draw_game_over_screen(screen, game, reset_btn_rect):
        screen.fill((117, 221, 221))

        text_color = (23, 42, 58)

        # Calculate the final scores
        ai_score = 0
        human_score = 0
        for r in range(const.ROWS):
            for c in range(const.COLS):
                if game.board[r][c] == const.BLACK_PIECE:
                    human_score += 1
                elif game.board[r][c] == const.WHITE_PIECE:
                    ai_score += 1
        
        # Determine the winner
        if ai_score > human_score:
            winner_text = "AI WINS!"
        elif human_score > ai_score:
            winner_text = "HUMAN WINS!"
        else:
            winner_text = "IT'S A DRAW!"
        
        # Draw the text
        title_font = pygame.font.SysFont(None, 80, bold=True)
        score_font = pygame.font.SysFont(None, 50)
        winner_font = pygame.font.SysFont(None, 60, bold=True)

        # Title
        title_text = title_font.render("GAME OVER", True, text_color)
        title_rect = title_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 5))
        screen.blit(title_text, title_rect)

        # Scores
        ai_score_text = score_font.render(f"AI (White): {ai_score}", True, text_color)
        ai_score_rect = ai_score_text.get_rect(center=(const.WIDTH // 2, title_rect.bottom + 60))
        screen.blit(ai_score_text, ai_score_rect)

        human_score_text = score_font.render(f"HUMAN (Black): {human_score}", True, const.WHITE)
        human_score_rect = human_score_text.get_rect(center=(const.WIDTH // 2, ai_score_rect.bottom + 30))
        screen.blit(human_score_text, human_score_rect)

        # Winner
        winner_text = winner_font.render(winner_text, True, text_color)
        winner_rect = winner_text.get_rect(center=(const.WIDTH // 2, human_score_rect.bottom + 60))
        screen.blit(winner_text, winner_rect)

        # DRAW THE START BUTTON COMPONENT
        # Draw the rectangle shape of the button
        pygame.draw.rect(screen, text_color, reset_btn_rect, border_radius=10)

        # Draw Play Again Button
        btn_font = pygame.font.SysFont(None, 40)
        btn_text = btn_font.render("PLAY AGAIN", True, const.WHITE)
        btn_text_rect = btn_text.get_rect(center=reset_btn_rect.center)
        screen.blit(btn_text, btn_text_rect)

    def run_game(self):
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

        # --- Create an instance of the AI ---
        # You can change difficulty_depth. 
        # 4 is decent. 5-6 is much stronger but slower.
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
            const.HEIGHT - 100, 
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
                self.draw_intro_screen(screen, start_btn_rect)
            elif game_state == "PLAYING":
                # --- Update display to show Human's last move ---
                # (We do this here so the player sees the board *before* the AI thinks)
                self.draw_board(screen)
                self.draw_pieces(screen, game.board)

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
                    self.draw_valid_moves(screen, valid_moves)

            elif game_state == "GAME_OVER":
                self.draw_game_over_screen(screen, game, reset_btn_rect)

            # --- Update Display ---
            pygame.display.flip()
            
            # --- Frame Limiting ---
            clock.tick(60)

        # --- Shutdown ---
        pygame.quit()

        sys.exit()

if __name__ == "__main__":
    ui = GameUI()
    ui.run_game()
