import pygame, csv
from config import *
from player import Player
from world import World

world = World()
player = Player(100,100,"World")
class Game:
    def __init__(self):
        self.create_world()

    def create_world(self):
        world_data = []
        for row in range(ROWS):
            r = [-1] * COLS
            world_data.append(r)

            with open ("img/test.csv", newLine='') as csvfile:
                reader = csv.reader(csvfile,delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            world.process_data(world_data)

    def main_loop(self):
        world.draw()
        player.draw()
        player_group.update()