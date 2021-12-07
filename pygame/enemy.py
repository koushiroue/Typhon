import pygame, os,random
from config import *
from player import Player

class Enemy (pygame.sprite.Sprite):
    def __init__(self,char_type, x, y,world):
        super().__init__()
        # Object
        self.world = world
        # Movement
        self.x = x
        self.y = y

        # Character Status
        self.alive = True;

        # Create Ai specific vraibles
        self.moveCounter = 0;
        self.vision = pygame.Rect(0, 0, 150, 20);
        self.idling = False;
        self.idlingCounter = 0;

        # load images
        self.animation_list = []
        self.animation_actions = ["idle", "walk","dead"]
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
            "death_front":8
        }

        self.import_character_assets()

        # Variables
        # Movement
        self.speed = 1
        self.direction = pygame.math.Vector2(0, 0)
        self.blocker = 1
        self.movement_loop = 1
        self.max_travel = random.randint(7, 200)

        #Health
        self.health = 100
        self.max_health = self.health




    def ai(self):
        if self.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                # 0: idle
                self.updateAction(self.perspective["default_front"])
                self.idling = True
                self.idlingCounter = 50;
                self.facing = random.choice([self.perspective["default_front"], self.perspective["default_back"], \
                                             self.perspective["default_right"], self.perspective["default_left"]])
            else:
                self.movement()


    def update(self):
        self.updateAnimation()
        self.checkAlive()
        if self.alive == True:
            self.check_collision()
            self.movement()

            self.direction.x = 0
            self.direction.y = 0


    def import_character_assets(self):
        for actions in self.animation_actions:
            for animations in self.animations_perspective:
                tempList = []
                # Count number of files in folder
                numOfFrames = len(os.listdir(os.path.join("img",f"{self.char_type}", f"{actions}", f"{animations}")))

                # loop through frames
                for i in range(numOfFrames):
                    img = pygame.image.load(
                        os.path.join("img",f"{self.char_type}", f"{actions}", f"{animations}", f"{i}.png")).convert_alpha()
                    tempList.append(img)
                self.animation_list.append(tempList)

            self.image = self.animation_list[self.action][self.frame_index]
            self.image = pygame.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.width = self.image.get_width()
            self.height = self.image.get_height()

    def checkAlive(self):
        if self.health <= 0:
            self.updateAction(self.perspective["death_front"]);
            self.health = 0;
            self.speed = 0;
            self.alive = False;
            print("ded")
            if self.world.player.facing == self.world.player.perspective["default_left"] \
                    or self.world.player.facing == self.world.player.perspective["default_right"]:
                self.rect.x += self.world.player.screenScroll
            elif self.world.player.facing == self.world.player.perspective["default_front"] \
                    or self.world.player.facing == self.world.player.perspective["default_back"]:
                self.rect.y += self.world.player.screenScroll

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
            if self.action == 8:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def movement(self):

        if self.facing == self.perspective["default_right"]:
            self.updateAction(self.perspective["right"])
            self.rect.x += self.speed * self.blocker
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice([self.perspective["default_front"], self.perspective["default_back"], \
                                             self.perspective["default_right"], self.perspective["default_left"]])

        if self.facing == self.perspective["default_left"]:
            self.updateAction(self.perspective["left"])
            self.rect.x -= self.speed * self.blocker
            self.movement_loop -= 1
            if self.movement_loop <= self.max_travel:
                self.facing = random.choice([self.perspective["default_front"], self.perspective["default_back"], \
                                             self.perspective["default_right"], self.perspective["default_left"]])

        if self.facing == self.perspective["default_front"]:
            self.updateAction(self.perspective["front"])
            self.rect.y += self.speed * self.blocker
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice([self.perspective["default_front"], self.perspective["default_back"], \
                                             self.perspective["default_right"], self.perspective["default_left"]])


        if self.facing == self.perspective["default_back"]:
            self.updateAction(self.perspective["back"])
            self.rect.y -= self.speed * self.blocker
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice([self.perspective["default_front"], self.perspective["default_back"], \
                                             self.perspective["default_right"], self.perspective["default_left"]])


    def check_collision(self):
        off_sets = 0
        # Check Collisions
        for tile in self.world.obstacleList:
            pygame.draw.rect(screen,WHITE,tile[1],3)
            # Cehck collision in the x axis
            if tile[1].colliderect(self.rect.x + off_sets, self.rect.y, self.width, self.height):
                pygame.draw.rect(screen, RED, self.rect, 3)
                if self.facing == self.perspective["default_right"]:
                    if self.rect.right > tile[1].left and self.rect.left < tile[1].left:
                        self.blocker = 0
                    else:
                        self.blocker = 1

            if tile[1].colliderect(self.rect.x - off_sets, self.rect.y, self.width, self.height):
                if self.facing == self.perspective["default_left"]:
                    pygame.draw.rect(screen, RED, self.rect, 3)
                    if self.rect.left < tile[1].right and self.rect.right > tile[1].right:
                        self.direction.x = 0
                    else:
                        self.direction.x = 1

            # Cehck collision in the y axis
            if tile[1].colliderect(self.rect.x, self.rect.y + off_sets, self.width, self.height):
                pygame.draw.rect(screen, RED, self.rect, 3)
                if self.facing == self.perspective["default_front"]:
                    if self.rect.bottom > tile[1].top and self.rect.top < tile[1].top:
                        self.blocker = 0
                    else:
                        self.blocker = 1

            if tile[1].colliderect(self.rect.x, self.rect.y - off_sets, self.width, self.height):
                pygame.draw.rect(screen, RED, self.rect, 3)
                if self.facing == self.perspective["default_back"]:
                    if self.rect.top < tile[1].bottom and self.rect.bottom > tile[1].bottom:
                        self.blocker = 0
                    else:
                        self.blocker = 1

            if pygame.sprite.spritecollide(self,water_group, False):
                pygame.draw.rect(screen, RED, self.rect, 3)
                self.speed = 2
            else:
                self.speed = 1

            if pygame.sprite.spritecollide(self,player_group, False):
                print("uwu enemy got hit")

        if self.world.player.facing == self.world.player.perspective["default_left"] \
                or self.world.player.facing == self.world.player.perspective["default_right"]:
            self.rect.x += self.world.player.screenScroll
        elif self.world.player.facing == self.world.player.perspective["default_front"] \
                or self.world.player.facing == self.world.player.perspective["default_back"]:
            self.rect.y += self.world.player.screenScroll


    def updateAction(self, newAction):
     # Check if the new action is different to the previous one
        if newAction != self.action:
            self.action = newAction

            # update the animation settings
            self.frame_index = 0;
            self.updateTime = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect, 3)
        screen.blit(self.image, self.rect);