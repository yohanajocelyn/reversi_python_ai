import pygame
import constants as const

# --- Game Drawing Class ---
# This class ONLY handles drawing to the screen.
# It uses "static methods" so we can call them without creating an instance.
class GameUI:
    WIDTH = const.WIDTH
    HEIGHT = const.HEIGHT

    @staticmethod
    def draw_intro_screen(screen, start_btn_rect):

        text_color = (23, 42, 58)

        screen.fill((117, 221, 221))
        
        # Set fontsnya
        title_font = pygame.font.SysFont(None, 80, bold=True)
        subtitle_font = pygame.font.SysFont(None, 40, italic=True)
        rules_font = pygame.font.SysFont(None, 28)
        btn_font = pygame.font.SysFont(None, 42, bold=True)

        # Title Text
        title_text = title_font.render("REVERSI", True, text_color)
        title_rect = title_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 5))
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

        start_y = subtitle_rect.bottom + 60
        for i, rule in enumerate(rules):
            rule_text = rules_font.render(rule, True, text_color)
            rule_rect = rule_text.get_rect(center=(const.WIDTH // 2, start_y + i * 35))
            screen.blit(rule_text, rule_rect)
        
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
            pygame.draw.line(screen, const.LINE_COLOR, (i * const.SQUARE_SIZE, 0), (i * const.SQUARE_SIZE, const.HEIGHT), 2)

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
