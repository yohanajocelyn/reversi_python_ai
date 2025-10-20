# main.py
import pygame
# from game.board import Board
# from game.reversi_ai import ReversiAI
from game.reversi_game import Game


# Main entry function
def main():
    game = Game()
    game.run_game()

if __name__ == "__main__":
    main()
