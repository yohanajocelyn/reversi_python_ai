import pygame
import constants as const

class GameView:
    """
    Handles all Pygame drawing.
    All methods are static, so we don't need to create an instance.
    """

    @staticmethod 
    def draw_intro_screen(screen, start_btn_rect):
        screen.fill(const.BG_COLOR)
        
        title_font = pygame.font.SysFont(None, 80, bold=True)
        subtitle_font = pygame.font.SysFont(None, 40, italic=True)
        rules_font = pygame.font.SysFont(None, 28)
        btn_font = pygame.font.SysFont(None, 42, bold=True)

        title_text = title_font.render("REVERSI", True, const.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 5))
        screen.blit(title_text, title_rect)

        subtitle_text = subtitle_font.render("Human vs AI", True, const.TEXT_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(const.WIDTH // 2, title_rect.bottom + 30))
        screen.blit(subtitle_text, subtitle_rect)

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
            rule_text = rules_font.render(rule, True, const.TEXT_COLOR)
            rule_rect = rule_text.get_rect(center=(const.WIDTH // 2, start_y + i * 35))
            screen.blit(rule_text, rule_rect)
        
        pygame.draw.rect(screen, const.TEXT_COLOR, start_btn_rect, border_radius=10)
        btn_font = pygame.font.SysFont(None, 40)
        btn_text = btn_font.render("START", True, const.WHITE)
        btn_rect = btn_text.get_rect(center=start_btn_rect.center)
        screen.blit(btn_text, btn_rect)

    @staticmethod
    def draw_board(screen):
        screen.fill(const.BOARD_COLOR)
        for i in range(const.ROWS + 1):
            pygame.draw.line(screen, const.LINE_COLOR, (0, i * const.SQUARE_SIZE), (const.WIDTH, i * const.SQUARE_SIZE), 2)
            pygame.draw.line(screen, const.LINE_COLOR, (i * const.SQUARE_SIZE, 0), (i * const.SQUARE_SIZE, const.HEIGHT), 2)

    @staticmethod
    def draw_pieces(screen, board_grid):
        """ 'board_grid' is the raw 8x8 list from the Board object """
        for row in range(const.ROWS):
            for col in range(const.COLS):
                piece = board_grid[row][col]
                if piece != const.EMPTY:
                    color = const.BLACK if piece == const.BLACK_PIECE else const.WHITE
                    center_x = col * const.SQUARE_SIZE + const.SQUARE_SIZE // 2
                    center_y = row * const.SQUARE_SIZE + const.SQUARE_SIZE // 2
                    pygame.draw.circle(screen, color, (center_x, center_y), const.PIECE_RADIUS)

    @staticmethod
    def draw_valid_moves(screen, moves_list):
        for row, col in moves_list:
            center_x = col * const.SQUARE_SIZE + const.SQUARE_SIZE // 2
            center_y = row * const.SQUARE_SIZE + const.SQUARE_SIZE // 2
            pygame.draw.circle(screen, const.VALID_MOVE_COLOR, (center_x, center_y), const.HINT_RADIUS)
    
    @staticmethod
    def draw_game_over_screen(screen, black_score, white_score, reset_btn_rect):
        """ Scoring logic is now done by the controller, this just draws """
        screen.fill(const.BG_COLOR)
        
        human_score = black_score
        ai_score = white_score

        if ai_score > human_score:
            winner_text_str = "AI WINS!"
        elif human_score > ai_score:
            winner_text_str = "HUMAN WINS!"
        else:
            winner_text_str = "IT'S A DRAW!"
        
        title_font = pygame.font.SysFont(None, 80, bold=True)
        score_font = pygame.font.SysFont(None, 50)
        winner_font = pygame.font.SysFont(None, 60, bold=True)

        title_text = title_font.render("GAME OVER", True, const.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 5))
        screen.blit(title_text, title_rect)

        ai_score_text = score_font.render(f"AI (White): {ai_score}", True, const.TEXT_COLOR)
        ai_score_rect = ai_score_text.get_rect(center=(const.WIDTH // 2, title_rect.bottom + 60))
        screen.blit(ai_score_text, ai_score_rect)

        human_score_text = score_font.render(f"HUMAN (Black): {human_score}", True, const.TEXT_COLOR)
        human_score_rect = human_score_text.get_rect(center=(const.WIDTH // 2, ai_score_rect.bottom + 30))
        screen.blit(human_score_text, human_score_rect)

        winner_text_obj = winner_font.render(winner_text_str, True, const.TEXT_COLOR)
        winner_rect = winner_text_obj.get_rect(center=(const.WIDTH // 2, human_score_rect.bottom + 60))
        screen.blit(winner_text_obj, winner_rect)

        pygame.draw.rect(screen, const.TEXT_COLOR, reset_btn_rect, border_radius=10)
        btn_font = pygame.font.SysFont(None, 40)
        btn_text = btn_font.render("PLAY AGAIN", True, const.WHITE)
        btn_text_rect = btn_text.get_rect(center=reset_btn_rect.center)
        screen.blit(btn_text, btn_text_rect)