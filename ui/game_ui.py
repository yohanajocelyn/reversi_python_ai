import pygame
from variables import constants as const

# --- Game Drawing Class ---
# This class ONLY handles drawing to the screen.
# It uses "static methods" so we can call them without creating an instance.
class GameUI:
    WIDTH = const.WIDTH
    HEIGHT = const.HEIGHT

    @staticmethod
    def draw_board(screen):
        """Draws the board background and grid lines."""
        screen.fill(const.BOARD_COLOR)
        for i in range(const.ROWS + 1):
            pygame.draw.line(screen, const.LINE_COLOR, (0, i * const.SQUARE_SIZE), (const.WIDTH, i * const.SQUARE_SIZE), 2)
            pygame.draw.line(screen, const.LINE_COLOR, (i * const.SQUARE_SIZE, 0), (i * const.SQUARE_SIZE, const.HEIGHT), 2)

    @staticmethod
    def draw_pieces(screen, board):
        """Draws all the pieces currently on the board."""
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
        """
        NEW FUNCTION: Draws hint dots for all valid moves.
        """
        for row, col in moves_list:
            center_x = col * const.SQUARE_SIZE + const.SQUARE_SIZE // 2
            center_y = row * const.SQUARE_SIZE + const.SQUARE_SIZE // 2
            pygame.draw.circle(screen, const.VALID_MOVE_COLOR, (center_x, center_y), const.HINT_RADIUS)