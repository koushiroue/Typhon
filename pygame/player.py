import pygame, os

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,world):
        super().__init__()
        self.x = x
        self.y = y
        self.world = world

        #anim var
        self.animation_list []
        self.animation_actions = ["idle","walk","attack","dead"]
        self.animation_perspective = ["Front","Back","Left","Right"]
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.facing = 0
        self.action = 0
        self.perspective = {
            "default_front": 0,
            "default_back": 1,
            "default_left": 2,
            "default_right": 3,
            "walk_front": 4,
            "walk_back": 5,
            "walk_left": 6,
            "walk_right": 7,
            "attack_front": 8,
            "attack_back": 9,
            "attack_left": 10,
            "attack_right": 11,
            "dead_front": 12
        }

        self.import_character_sprites()

        #movement variable
        self.speed = 3
        self.direction = pygame.math.Vector2(0,0)
        self.dx = 0
        self.dy = 0

        #screen variable
        self.screen_scroll = screen_scroll
        self.SCROLLTHRESHOLD = SCROLLTHRESHOLD

    def update(self):
        self.update_animation()
        self.get_key_inut()
        self.movement()
        self.direction.x = 0
        self.direction.y = 0

    def get_key_input(self):
        keys = pygame.key.get_pressed()
        #buttons = pygame.mouse,get_pressed()

        #Walking front + back
        if keys[pygame.K_s]:
            self.update_action(self.perspective["walk_front"])
            self.direction.y = 1
            self.facing = self.perspective["default_front"]
        elif keys[pygame.K_w]:
            self.update_action(self.perspective["walk_back"])
            self.direction.y = -1
            self.facing = self.perspective["default_back"]
        else:
            if self.facing = self.perspective["default_front"]:
                self.update_action(self.perspective["default_front"])
            if self.facing = self.perspective["default_back"]:
                self.update_action(self.perspective["default_back"])
        #Walking left + right
        if keys[pygame.K_d]:
            self.update_action(self.perspective["walk_right"])
            self.direction.x = 1
            self.facing = self.perspective["default_right"]
        elif keys[pygame.K_a]:
            self.update_action(self.perspective["walk_left"])
            self.direction.x = -1
            self.facing = self.perspective["default_left"]

    def import_character_sprites(self):
        for actions in self.animation_actions:
            for animations in self.animation_perspective:
                temp_list = []
                #count the frames of animations
                num_of_frames = len(os.listdir(\
                    os.path.join("img","Player",f"{actions}",f"{animations}")))

                #loop animation
                for i in range(num_of_frames):
                    img = pygame.image.load(\
                        os.path.join("img","Player",f"{actions}",f"{animations}",f"{i}.png")).convert_alpha()
                    temp_list.append(img)
                self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.image = pygame.transform.scale(self.image,(TILESIZE * 2, TILESIZE * 2))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x,self.y)
            self.width = self.image.get.width()
            self.height = self.image.get.height()

        def update_action(self.new_action):
            #check current action is diff than old
            if new_action =! self.action:
                self.action = new_action

                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def movement(self):
            self.rect.x += self.direction.x * self.speed + self.dx
            self.rect.y += self.direction.y * self.speed + self.dy




        def update_animation(self):
            #Anim cooldown
        ANIMATIONCOOLDOWN = 100

        self.image = self.animation_list[self.action].self.frame_index]
        self.image = pygame.transform.scale(self.image, TILESIZE * 2, TILESIZE * 2))

        if pygame.time.get_ticks() - self.update_time > ANIMATIONCOOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

    #restart anim
    if self.frame_index >= len(self.animation_list[self.action]):
        if self.action == self.perspective["dead_front"]:
        self.frame_index = len(self.animation_list[self.action]) - 1
    elif self.action >= 8 and self.action <= 11:
        if self.action == 8:
            self.frame_index = len(self.animation_list[self.action]) - 1
            self.perspective["default_front"]
        elif self.action == 9:
            self.frame_index = len(self.animation_list[self.action]) - 1            self.perspective["default_front"]
            self.perspective["default_back"]
        elif self.action == 10:
            self.frame_index = len(self.animation_list[self.action]) - 1            self.perspective["default_front"]
            self.perspective["default_left"]
        elif self.action == 11:
            self.frame_index = len(self.animation_list[self.action]) - 1            self.perspective["default_front"]
            self.perspective["default_right"]
    else:
        self.frame_index = 0

    def movement(self):
        self.rect.x += self.direction.x * self.speed * self.dx
        self.rect.y += self.direction.y * self.speed * self.dy

    def check_collision(self):
        offset = 7
        for tile in self.world.obstacle_list:
            pygame.draw.rect(screen, WHITE, tile[1],3)
            if tile[1].colliderect(self.rect.x - offset, self.rect.y, self.widt, self.height):
                if self.facing = self.perspective["default_right"]:
                    if self.rect.right > tile[1].left or self.rect.left < tile[1].left:
                        self.direction.x = 0
                    else:
                        self.direction.x = 1
                if self.facing = self.perspective["default_left"]:
                    if self.rect.right > tile[1].right or self.rect.left < tile[1].right:
                        self.direction.y = 0
                    else:
                        self.direction.y = 1
                if self.facing = self.perspective["default_front"]:
                    if self.rect.top > tile[1].bottom or self.rect.bottom < tile[1].bottom:
                        self.direction.y = 0
                    else:
                        self.direction.y = 1



        def draw(self)
            #hitbox
            pygame.draw.rect(screen, WHITE, self.rect, 3)
            screen.blit(self.image, self.rect)
