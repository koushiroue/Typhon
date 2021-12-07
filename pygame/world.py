import pygame
from config import *
from player import Player


class Beach(pygame.sprite.Sprite):
    def __init__(self,img,x,y,world):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.x = x
        self.y = y
        self.world = world
        self.width = TILESIZE
        self.height = TILESIZE
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.player.facing == self.player.perspective["default_front"] or \
                self.player.facing == self.player.perspective["default_back"]:
            tile[1][1] == self.player.screen_scroll

        elif self.player.facing == self.player.perspective["default_left"] or \
                self.player.facing == self.player.perspective["default_right"]:
            tile[1][1] == self.player.screen_scroll


class World:
    def __init__(self):
        self.obstacle_list = []
        self.scroll = 0

    def process_data(self,data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = imgList[tile]
                    img_rect = img.get_rect()
                    img.rect.x = x * TILESIZE * 2
                    img_rect.y = y * TILESIZE * 2
                    tile_data = (img,img_rect)
                    if tile == 0:
                        self.obstacle_list.append(tile_data)
                        if tile == 1:
                            water = Water(img,x * TILESIZE * 2, y * TILESIZE * 2, self)

                        if tile == 2:
                            self.player = Player(x * TILESIZE * 2, y * TILESIZE * 2, self)
                            player_group.add(water)
                            if tile == 3:
                                pass
                            if tile >= 4 and tile <= 7:
                                beach = Beach(img,x * TILESIZE * 2, y * TILESIZE * 2, self)
                                beach_gruop.add(beach)
            def draw(self):
                for tile in self.obstacle_list:
                    if self.player.facing == self.player.perspective["default_front"] or\
                            self.player.facing == self.player.perspective["default_back"]:
                        tile[1][1] == self.player.screen_scroll

                    elif self.player.facing == self.player.perspective["default_left"] or\
                            self.player.facing == self.player.perspective["default_right"]:
                        tile[1][1] == self.player.screen_scroll

                    screen.blit(tile[0],tile[1])
