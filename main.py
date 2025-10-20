# main.py
import pygame
from game.board import Board
from game.reversi_ai import ReversiAI
from ui.game_ui import GameUI

# Main entry function
def main():
    pygame.init()
    pygame.display.set_caption("Reversi - Human vs AI")

    # Create a clock to control FPS
    clock = pygame.time.Clock()

    # Initialize game components
    board = Board()
    ai = ReversiAI(color='black')  # AI plays black
    ui = GameUI(board)

    running = True
    current_turn = 'white'  # Human starts

    while running:
        ui.draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Human move
            if current_turn == 'white':
                move = ui.handle_click(event)
                if move and board.is_valid_move(move, 'white'):
                    board.place_piece(move, 'white')
                    current_turn = 'black'

        # AI move
        if current_turn == 'black' and not board.is_game_over():
            pygame.time.delay(500)  # Small pause for realism
            ai_move = ai.choose_move(board)
            if ai_move:
                board.place_piece(ai_move, 'black')
            current_turn = 'white'

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
