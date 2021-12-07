import pygame
from button add Button
from config import *
class Menu:
    def __init__(self):
        self.start_button = button("NEW GAME",100,100,(WIDTH//2 + 100, HEIGHT//2 - 500), 2)
        self.exit_button = button("EXIT",100,100,(WIDTH//2 + 100, HEIGHT//2 - 500), 2)