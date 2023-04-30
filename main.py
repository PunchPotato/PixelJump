import pygame
from pygame.locals import *
import sys

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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect()

        self.pos = vec((200, 100))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self):
        global jump
        self.acc = vec(0, 0.35)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -acceleration
        if pressed_keys[K_RIGHT]:
            self.acc.x = acceleration

        self.acc.x += self.vel.x * friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width
        if self.vel.y > 0:
            jump = True
        elif self.vel.y < 0:
            jump = False

        self.rect.midbottom = self.pos

    def update(self):
        global pass_through_check

        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if hits and jump == True:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            P1.jump()

    def jump(self):
        global pass_through_check
        global jump
        if jump:
            self.vel.y = -15


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((width, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(width / 2, height - 400))


class Platform2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = pygame.Surface((100, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(width / 2, height - 590))


P1 = Player()
PT1 = Platform()
PT2 = Platform2()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(PT1)
all_sprites.add(PT2)

platforms = pygame.sprite.Group()
platforms.add(PT1)
platforms.add(PT2)

while True:
    screen.fill(pygame.Color("black"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            sys.exit()

    P1.move()
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    P1.update()
    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
