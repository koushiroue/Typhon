import pygame, os, random
from config import *
from slash import Slash
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y,world):
        super().__init__()
        #Object
        self.world = world
        #Movement
        self.x = x
        self.y = y

        #Character Status
        self.alive = True;

        # load images
        self.animation_list = []
        self.animation_actions = ["idle", "walk","attack","dead"]
        self.animations_perspective = ["Front", "Back", "Left", "Right"]
        self.char_type = char_type
        self.action = 0
        self.frame_index = 0
        self.updateTime = pygame.time.get_ticks()
        self.facing = 0

        self.perspective = {
            "default_front": 0,
            "default_back": 1,
            "default_left": 2,
            "default_right": 3,
            "front": 4,
            "back": 5,
            "left": 6,
            "right": 7,
            "attack_front":8,
            "attack_back":9,
            "attack_left":10,
            "attack_right":11,
            "death_front": 12
        }

        self.import_character_assets()

        # Variables
        # Movement
        self.speed = 3
        self.direction = pygame.math.Vector2(0, 0)
        self.dx = 0
        self.dy = 0
        self.screenScroll = screenScroll
        self.SCROLLTRESHOLD = SCROLLTHRESH

        # Health
        self.health = 1000;
        self.maxHealth = self.health;

        #Cooldown
        self.shootCooldown = 0

        #Clicked
        self.clicked = False


    def update(self):
        self.updateAnimation()
        self.checkAlive()
        if self.alive == True:
            self.get_key_input()
            self.check_collision()
            self.movement()
            self.check_scroll()

            self.direction.x = 0
            self.direction.y = 0

            if self.shootCooldown > 0:
                self.shootCooldown -= 1;

    def import_character_assets(self):
        for actions in self.animation_actions:
            for animations in self.animations_perspective:
                tempList = []
                # Count number of files in folder
                numOfFrames = len(os.listdir(os.path.join("img",f"{self.char_type}", f"{actions}", f"{animations}")))

                # loop through frames
                for i in range(numOfFrames):
                    img = pygame.image.load(os.path.join("img",f"{self.char_type}", f"{actions}", f"{animations}", f"{i}.png")).convert_alpha()
                    tempList.append(img)
                self.animation_list.append(tempList)

            self.image = self.animation_list[self.action][self.frame_index]
            self.image = pygame.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.width = self.image.get_width()
            self.height = self.image.get_height()

    def updateAnimation(self):
        # update animation
        ANIMATIONCOOLDOWN = 100;

        # Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        self.image = pygame.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))

        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.updateTime > ANIMATIONCOOLDOWN:
            self.updateTime = pygame.time.get_ticks()
            self.frame_index += 1

        # If the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 12:
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif self.action >= 8 and self.action <= 11:
                if self.action == 8:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                    self.updateAction(self.perspective["default_front"])
                elif self.action == 9:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                    self.updateAction(self.perspective["default_back"])
                elif self.action == 10:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                    self.updateAction(self.perspective["default_left"])
                elif self.action == 11:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                    self.updateAction(self.perspective["default_right"])
            else:
                self.frame_index = 0

    def movement(self):
        self.rect.x += self.direction.x * self.speed + self.dx
        self.rect.y += self.direction.y * self.speed + self.dy


    def check_collision(self):
        tile_test = []
        off_sets = 7
        # Check Collisions
        for tile in self.world.obstacleList:
            tile_test.append(tile)
            pygame.draw.rect(screen,WHITE,tile[1],3)
            # Cehck collision in the x axis
            if tile[1].colliderect(self.rect.x + off_sets,self.rect.y,self.width,self.height):
                pygame.draw.rect(screen, RED, self.rect,3)
                if self.facing == self.perspective["default_right"]:
                    if self.rect.right > tile[1].left or self.rect.left < tile[1].left:
                        self.direction.x = 0
                    else:
                        self.direction.x = 1

            if tile[1].colliderect(self.rect.x - off_sets,self.rect.y,self.width,self.height):
                if self.facing == self.perspective["default_left"]:
                    pygame.draw.rect(screen, RED, self.rect, 3)
                    if self.rect.left < tile[1].right or self.rect.right > tile[1].right:
                        self.direction.x = 0
                    else:
                        self.direction.x = -1

            # Cehck collision in the y axis
            if tile[1].colliderect(self.rect.x,self.rect.y + off_sets,self.width,self.height):
                pygame.draw.rect(screen, RED, self.rect,3)
                if self.facing == self.perspective["default_front"]:
                    if self.rect.bottom > tile[1].top or self.rect.top < tile[1].top:
                        self.direction.y = 0
                    else:
                        self.direction.y = 1

            if tile[1].colliderect(self.rect.x,self.rect.y - off_sets,self.width,self.height):
                pygame.draw.rect(screen, RED, self.rect,3)
                if self.facing == self.perspective["default_back"]:
                    if self.rect.top < tile[1].bottom or self.rect.bottom > tile[1].bottom:
                        self.direction.y = 0
                    else:
                        self.direction.y = -1

            if pygame.sprite.spritecollide(self,water_group, False):
                pygame.draw.rect(screen, RED, self.rect, 3)
                self.speed = 1

            if pygame.sprite.spritecollide(self,enemy_group, False):
                pygame.draw.rect(screen, RED, self.rect, 3)
                print("Collided")
                self.health -= 1

            if self.rect.right > WIDTH:
                self.dx = WIDTH - self.rect.right
            elif self.rect.left < 0:
                self.dx = self.rect.right
            else:
                self.dx = 0

            if self.rect.top < 0:
                self.dy = self.rect.bottom
            elif self.rect.bottom > HEIGHT:
                self.dy = HEIGHT - self.rect.bottom
            else:
                self.dy = 0

    def check_scroll(self):
        if self.direction.x > 0 and self.rect.x >  self.SCROLLTRESHOLD:
            self.screenScroll = -3

        elif self.direction.x < 0 and self.rect.x >  -self.SCROLLTRESHOLD:
            self.screenScroll = 3

        elif self.direction.y > 0 and self.rect.y >  self.SCROLLTRESHOLD:
            self.screenScroll = -3

        elif self.direction.y < 0 and self.rect.y >  -self.SCROLLTRESHOLD:
            self.screenScroll = 3
        else:
            self.screenScroll = 0


    def updateAction(self, newAction):
     # Check if the new action is different to the previous one
        if newAction != self.action:
            self.action = newAction

            # update the animation settings
            self.frame_index = 0;
            self.updateTime = pygame.time.get_ticks()

    def get_key_input(self):
        keys = pygame.key.get_pressed()

        #left and right
        if keys[pygame.K_d]:
            self.updateAction(self.perspective["right"])
            self.direction.x = 1
            self.facing = self.perspective["default_right"]

        elif keys[pygame.K_a]:
            self.updateAction(self.perspective["left"])
            self.direction.x = -1
            self.facing = self.perspective["default_left"]

        #up and down
        elif keys[pygame.K_w]:
            self.updateAction(self.perspective["back"])
            self.direction.y = -1
            self.facing = self.perspective["default_back"]

        elif keys[pygame.K_s]:
            self.updateAction(self.perspective["front"])
            self.direction.y = 1
            self.facing = self.perspective["default_front"]

        else:
            #Check if standing still
            #Right and left
            if self.facing == self.perspective["default_right"]:
                self.updateAction(self.perspective["default_right"])
            elif self.facing == self.perspective["default_left"]:
                self.updateAction(self.perspective["default_left"])

            #Back and front
            if self.facing == self.perspective["default_back"]:
                self.updateAction(self.perspective["default_back"])
            elif self.facing == self.perspective["default_front"]:
                self.updateAction(self.perspective["default_front"])

        #Sprinting
        if keys[pygame.K_LSHIFT]:
            self.speed = 10
        else:
            self.speed = 3

        if keys[pygame.K_SPACE]:
            if self.facing == self.perspective["default_front"]:
                self.updateAction(self.perspective["attack_front"])
                self.facing = self.perspective["attack_front"]
                self.attack()

            elif self.facing == self.perspective["default_back"]:
                  self.updateAction(self.perspective["attack_back"])
                  self.facing = self.perspective["attack_back"]
                  self.attack()

            elif self.facing == self.perspective["default_left"]:
                  self.updateAction(self.perspective["attack_left"])
                  self.facing = self.perspective["attack_left"]
                  self.attack()

            elif self.facing == self.perspective["default_right"]:
                  self.updateAction(self.perspective["attack_right"])
                  self.facing = self.perspective["attack_right"]
                  self.attack()
        else:
            if self.facing == self.perspective["attack_front"]:
                self.facing = self.perspective["default_front"]
            elif self.facing == self.perspective["attack_back"]:
                self.facing = self.perspective["default_back"]
            elif self.facing == self.perspective["attack_left"]:
                self.facing = self.perspective["default_left"]
            elif self.facing == self.perspective["attack_right"]:
                self.facing = self.perspective["default_right"]

    def attack(self):
        if self.shootCooldown == 0:
            self.shootCooldown = 70
            slash= Slash(self.rect.x + 20, self.rect.y,1,self.world);
            slash_group.add(slash)


    def checkAlive(self):
        if self.health <= 0:
            self.updateAction(self.perspective["death_front"]);
            self.health = 0;
            self.speed = 0;
            self.alive = False;
            print("ded")

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect, 3)
        screen.blit(self.image, self.rect);






