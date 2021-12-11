import pygame

from game import *

g = Game()
g.intro()

while g.running:
    # display menu
    g.curr_menu.display_menu()
    # loop game(???)
    g.game_loop()
