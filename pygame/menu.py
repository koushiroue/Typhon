import pygame, os
from button import Button
from config import *

class Menu:
    def __init__(self):
        self.startButton = Button("Start", 500, 100, (WIDTH // 2-240, HEIGHT // 2-200), 2)
        self.exitButton = Button("Exit", 500, 100, (WIDTH // 2-240, HEIGHT // 2 + 100), 2)