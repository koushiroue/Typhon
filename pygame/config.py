import pygame
import os

#Global Variables
#Screen size
WIDTH = 1152
HEIGHT = 648

# screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Workshop")

#TILESIZE
TILESIZE = 32
TILETYPES = 8

#Groups
enemy_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
beach_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
slash_group = pygame.sprite.Group()

#load attack images
front_slash_image = pygame.image.load(os.path.join("img","icons","front.png")).convert_alpha();
front_slash_image = pygame.transform.scale(front_slash_image,(TILESIZE*2,TILESIZE*2)).convert_alpha();
back_slash_image = pygame.image.load(os.path.join("img","icons","back.png")).convert_alpha();
back_slash_image = pygame.transform.scale(back_slash_image,(TILESIZE*2,TILESIZE*2)).convert_alpha();
left_slash_image = pygame.image.load(os.path.join("img","icons","left.png")).convert_alpha();
right_slash_image = pygame.image.load(os.path.join("img","icons","right.png")).convert_alpha();


#Store tiles in a list
imgList = []
for x in range(TILETYPES):
    img = pygame.image.load(os.path.join("img","tile",f"{x}.png")).convert_alpha();
    img = pygame.transform.scale(img,(TILESIZE *2,TILESIZE*2));
    imgList.append(img)



#FPS
FPS = 60

#Clock
clock = pygame.time.Clock()

#game variables
running = True
start_game = False

#World
SCROLLTHRESH = 10
screenScroll = 0
bgScroll = 0
ROWS = 50
COLS = 50

#Colour
RED = (255,0,0)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BG_COLOUR = (255, 242, 204)
