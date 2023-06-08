import pygame
from pygame.locals import *
import sys
import random

width = 580
height = 920
fps = 60
acceleration = 0.5
friction = - 0.12
vec = pygame.math.Vector2
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pass_through_check = False
jump = False
plat_img = pygame.image.load("graphic/groundy ground.png").convert_alpha()
max_platforms = 10
scroll_height = 300
higher_scroll_height = 0
scroll = 0
bg_scroll = 0
bg_image = pygame.image.load("graphic/silly background.png").convert_alpha()
#bg_image_big = pygame.transform.scale(bg_image, (580, 920))
sprite_1 = pygame.image.load("graphic/CAT SPRITE  DARK 1.png").convert_alpha()
sprite_2 = pygame.image.load("graphic/CAT SPRITE  DARK 2.png").convert_alpha()
time = pygame.time.get_ticks()
spring_img = pygame.Surface((20, 20))
spring_img.fill("black")
max_springs = 2
score = 0
score_line = pygame.image.load("graphic/score background.png").convert_alpha()


def get_font(size):
    return pygame.font.Font("TenOClockRegular-8L7n.ttf", size)


def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -920 + bg_scroll))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = sprite_1
        self.rect = self.surf.get_rect()

        self.pos = vec((300, 800))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.fog = pygame.image.load("graphic/foggy.png").convert_alpha()
        self.spot_light = pygame.image.load("graphic/Spot Light.png").convert_alpha()

    def move(self):
        global jump
        global scroll
        scroll = 0
        self.acc = vec(0, 0.35)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -acceleration - 0.1
        if pressed_keys[K_RIGHT]:
            self.acc.x = acceleration + 0.1

        self.acc.x += self.vel.x * friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        if self.vel.y > 5:
            jump = True
        elif self.vel.y < 0:
            jump = False

        if self.pos.y > 1000:
            pygame.quit()

        self.rect.midtop = self.pos

        if self.rect.top <= scroll_height:
            if self.vel.y <= 0:
                self.pos.y = scroll_height
                scroll = -self.vel.y

        return scroll

    def update(self):
        global pass_through_check
        global time
        global score
        hits = pygame.sprite.spritecollide(P1, platform_group, False)
        hits_spring = pygame.sprite.spritecollide(P1, spring_group, False)
        if scroll:
            score += 2
        text = get_font(70).render(str(score), True, "black")
        text_rect = text.get_rect()
        text_rect.center = (width // 8, height // 18)
        screen.blit(text, text_rect)
        if hits and jump == True:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            P1.jump()
            self.surf = sprite_2
            time = 0

        if hits_spring and jump == True:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            P1.spring_jump()
            self.surf = sprite_2
            time = 0

        elif self.vel.y > 0:
            self.surf = sprite_1

    def jump(self):
        global pass_through_check
        global jump
        if jump:
            self.vel.y = -15

    def spring_jump(self):
        if jump:
            self.vel.y = -40

    def light_effect(self):
        screen.blit(self.fog, (0, 0))
        screen.blit(self.spot_light, self.rect)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x2, y2):
        pygame.sprite.Sprite.__init__(self)
        self.image = plat_img
        self.rect = self.image.get_rect()
        self.rect.x = x2
        self.rect.y = y2

    def update(self, scroll):

        self.rect.y += scroll

        if self.rect.top > height:
            self.kill()


class Spring(pygame.sprite.Sprite):
    def __init__(self, x2, y2):
        pygame.sprite.Sprite.__init__(self)
        self.image = spring_img
        self.rect = self.image.get_rect()
        self.rect.x = x2
        self.rect.y = y2

    def update(self, scroll):
        self.rect.y += scroll

        if self.rect.top > height:
            self.kill()


platform_group = pygame.sprite.Group()

platform = Platform(width // 2 - 50, height - 50)
platform_group.add(platform)

P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)

spring_group = pygame.sprite.Group()
spring = Spring(400, -980)
spring_group.add(spring)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            sys.exit()

    bg_scroll += scroll
    if bg_scroll >= height:
        bg_scroll = 0
    draw_bg(bg_scroll)
    time += 1
    platform_group.update(scroll)

    if len(platform_group) < max_platforms:
        p_x = random.randint(0, 500)
        p_y = platform.rect.y - random.randint(80, 200)
        platform = Platform(p_x, p_y)
        platform_group.add(platform)

    #if len(spring_group) < max_springs:
        #s_x = random.randint(0, 500)
        #s_y = spring.rect.y - random.randint(80, 200)
        #spring = Spring(s_x, s_y)
        #platform_group.add(spring)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    platform_group.draw(screen)
    P1.light_effect()
    screen.blit(score_line, (0, 0))
    P1.move()
    P1.update()
    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
