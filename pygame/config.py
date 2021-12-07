import pygame, os

#init pygame
pygame.init()

#Screen Size
HEIGHT = 1152
WIDTH = 648

#init screen
screen = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("Typhon")

#Sprite Group
player_group = pygame.sprite.group.Group()
water_group = pygame.sprite.Group()
beach_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

#screen misc
screen_scroll = 0
SCROLLTRESHOLD = 16
FPS = 60
clock = pygame.time.Clock()

#game var
running = true
start_game = False
TILESIZE = 32
TILETYPES = 8
ROWS = 50
COLS = 50

img_list = []
for x in range(TILETYPES):
    img = pygame.image.load(os.path.join("img","tile",f"{x}.png")).convert_alpha()
    img = pygame.transform.scale(img,(TILESIZE * 2, TILESIZE * 2))
    img_list.append(img)



WHITE = (255,255,255)