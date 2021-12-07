import pygame, os
from config import *
from player import Player
from Enemy import Enemy
from healthbar import HealthBar
#########################################################################################################################################
class Beach(pygame.sprite.Sprite):
    def __init__(self, img,  x, y,world):
        pygame.sprite.Sprite.__init__(self);
        # Movement
        self.image = img;
        self.x = x
        self.y = y
        self.world = world
        self.width = TILESIZE
        self.height = TILESIZE
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.world.player.facing == self.world.player.perspective["default_left"] \
                or self.world.player.facing == self.world.player.perspective["default_right"]:
                    self.rect.x += self.world.player.screenScroll
        elif self.world.player.facing == self.world.player.perspective["default_front"] \
                or self.world.player.facing == self.world.player.perspective["default_back"]:
            self.rect.y += self.world.player.screenScroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img,  x, y,world):
        pygame.sprite.Sprite.__init__(self);
        # Movement
        self.image = img;
        self.x = x
        self.y = y
        self.world = world
        self.width = TILESIZE
        self.height = TILESIZE
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.world.player.facing == self.world.player.perspective["default_left"] \
                or self.world.player.facing == self.world.player.perspective["default_right"]:
                    self.rect.x += self.world.player.screenScroll
        elif self.world.player.facing == self.world.player.perspective["default_front"] \
                or self.world.player.facing == self.world.player.perspective["default_back"]:
            self.rect.y += self.world.player.screenScroll



class World():
    def __init__(self):
        self.obstacleList = []
        self.scroll = 0

    def processData(self,data):
        #Get level length
        self.levelLength = len(data[0]);
        #Iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = imgList[tile]
                    imgRect = img.get_rect();
                    imgRect.x = x * TILESIZE *2;
                    imgRect.y = y * TILESIZE *2;
                    tileData = (img,imgRect);
                    if tile == 0:
                        self.obstacleList.append(tileData);
                    if tile == 1:
                        water = Water(img, x * TILESIZE * 2, y * TILESIZE * 2,self);
                        water_group.add(water)
                    if tile == 2:
                        self.player = Player("player", x * TILESIZE * 2,y * TILESIZE * 2,self)
                        player_group.add(self.player)
                        self.healthbar = HealthBar(10, 10, self.player.health, self.player.health)
                    if tile == 3:
                        enemy = Enemy("enemy", x * TILESIZE * 2,y * TILESIZE * 2,self)
                        enemy_group.add(enemy)
                    if tile >= 4 and tile <= 7:
                        beach = Beach(img, x * TILESIZE * 2, y * TILESIZE * 2, self);
                        beach_group.add(beach)



    def draw(self):
        for tile in self.obstacleList:
            if self.player.facing == self.player.perspective["default_left"]\
                or self.player.facing == self.player.perspective["default_right"]:
                    tile[1][0] += self.player.screenScroll
            elif self.player.facing == self.player.perspective["default_front"] \
                    or self.player.facing == self.player.perspective["default_back"]:
                    tile[1][1] += self.player.screenScroll
            screen.blit(tile[0],tile[1]);
            self.healthbar.draw(self.player.health)


