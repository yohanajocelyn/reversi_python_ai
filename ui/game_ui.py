import pygame
import sys

class GameUI:
    # --- Constants ---

    # Board dimensions
    ROWS = 8
    COLS = 8

    # Size of each square on the board (in pixels)
    SQUARE_SIZE = 80

    # Total window dimensions
    WIDTH = COLS * SQUARE_SIZE
    HEIGHT = ROWS * SQUARE_SIZE

    # Piece representation (using numbers for the 2D array)
    EMPTY = 0
    BLACK_PIECE = 1
    WHITE_PIECE = 2

    # Colors (RGB)
    BOARD_COLOR = (0, 128, 0)      # A classic "felt green"
    LINE_COLOR = (0, 0, 0)         # Black grid lines
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Radius of the game pieces
    # We make it slightly smaller than the square's half-size for a nice margin
    PIECE_RADIUS = SQUARE_SIZE // 2 - 5

    # --- Board Data Structure ---

    def run_game():
        # Initialize all Pygame modules
        pygame.init()
        
        # Set up the game window
        screen = pygame.display.set_mode((GameUI.WIDTH, GameUI.HEIGHT))
        pygame.display.set_caption("Othello (Reversi) Board")
        
        # Set up the game clock to control FPS
        clock = pygame.time.Clock()
        
        # Create the initial board state
        board = GameUI.create_board()

        running = True
        while running:
            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # This is where you would add game logic
                    # For example, get the mouse position:
                    # mouse_x, mouse_y = pygame.mouse.get_pos()
                    #
                    # Convert pixel coordinates to board (row, col)
                    # row = mouse_y // SQUARE_SIZE
                    # col = mouse_x // SQUARE_SIZE
                    #
                    # Then, check if the move is valid and update the board
                    # (Logic not included in this UI-only example)
                    pass

            # --- Drawing ---
            # 1. Draw the static board (background and grid)
            GameUI.draw_board(screen)
            
            # 2. Draw the pieces on top of the board
            GameUI.draw_pieces(screen, board)

            # --- Update Display ---
            # Flip the display buffer to show the new frame
            pygame.display.flip()
            
            # --- Frame Limiting ---
            # Wait for the next frame, limiting to 60 FPS
            clock.tick(60)

        # --- Shutdown ---
        pygame.quit()
        sys.exit()

    def create_board():
        """
        Initializes the 8x8 board grid and places the
        four starting pieces in the center.
        """
        # Create an 8x8 grid filled with EMPTY (0)
        board = [[GameUI.EMPTY] * GameUI.COLS for _ in range(GameUI.ROWS)]

        # Place the four starting pieces
        board[3][3] = GameUI.WHITE_PIECE
        board[3][4] = GameUI.BLACK_PIECE
        board[4][3] = GameUI.BLACK_PIECE
        board[4][4] = GameUI.WHITE_PIECE
        
        return board

    # --- Drawing Functions ---

    def draw_board(screen):
        """
        Draws the board background and grid lines.
        """
        # 1. Fill the entire screen with the board color
        screen.fill(GameUI.BOARD_COLOR)
        
        # 2. Draw the grid lines
        # We draw 9 vertical and 9 horizontal lines to create 8x8 squares
        for i in range(GameUI.ROWS + 1):
            # Horizontal lines
            pygame.draw.line(screen, 
                            GameUI.LINE_COLOR,                # Color
                            (0, i * GameUI.SQUARE_SIZE),      # Start point (x, y)
                            (GameUI.WIDTH, i * GameUI.SQUARE_SIZE),  # End point (x, y)
                            2)                         # Line width
            # Vertical lines
            pygame.draw.line(screen, 
                            GameUI.LINE_COLOR,                # Color
                            (i * GameUI.SQUARE_SIZE, 0),      # Start point (x, y)
                            (i * GameUI.SQUARE_SIZE, GameUI.HEIGHT), # End point (x, y)
                            2)                         # Line width

    def draw_pieces(screen, board):
        """
        Draws all the pieces currently on the board.
        """
        # Iterate over every square in the 2D board array
        for row in range(GameUI.ROWS):
            for col in range(GameUI.COLS):
                piece = board[row][col]
                
                # Check if the square is not empty
                if piece != GameUI.EMPTY:
                    # Determine the color based on the piece type
                    color = GameUI.BLACK if piece == GameUI.BLACK_PIECE else GameUI.WHITE
                    
                    # Calculate the (x, y) center of the circle
                    # We add SQUARE_SIZE // 2 to the top-left corner of the square
                    center_x = col * GameUI.SQUARE_SIZE + GameUI.SQUARE_SIZE // 2
                    center_y = row * GameUI.SQUARE_SIZE + GameUI.SQUARE_SIZE // 2
                    
                    # Draw the circle
                    pygame.draw.circle(screen, 
                                    color,           # Color
                                    (center_x, center_y), # Center (x, y)
                                    GameUI.PIECE_RADIUS)    # Radius


    # This ensures the main() function runs only when the script is executed directly
    if __name__ == "__main__":
        main()