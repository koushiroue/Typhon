import pygame, os
from config import *
from game import Game
from menu import Menu

pygame.mixer.init()
pygame.mixer.music.load(os.path.join("audio", "bg_music.wav"))

game = Game()

if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            #quit window / app
            if event.type == pygame.QUIT:
                running == False

        screen.fill(WHITE)
        game.main_loop()



                pygame.display.update()
                clock.tick(FPS)
pygame.quit()
exit()