import pygame
from game import Game
from config import *
from menu import Menu

game = Game()
m = Menu()

if __name__ == "__main__":
    while running:

        # Event Checker
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                running = False

        if start_game == False:
            screen.fill("white")
            if m.startButton.draw(screen):
                start_game = True
            if m.exitButton.draw(screen):
                running = False
                start_game = False
        else:
            game.main_loop()


        pygame.display.update()
        clock.tick(FPS)
pygame.quit();
exit();