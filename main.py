import pygame
import thorpy

from game import *

g = Game()

while g.running:
    g.intro()
    # display menu
    g.curr_menu.display_menu()
    # loop game(???)
    g.game_loop()
