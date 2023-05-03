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
plat_img = pygame.Surface((100, 20))
plat_img.fill("red")
MAX_PLATFORMS = 10
SCROLL_THRESH = 200
scroll = 0
bg_scroll = 0
bg_image = pygame.image.load("graphic/background.png").convert_alpha()


def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect()

        self.pos = vec((200, 400))
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

        if self.vel.y > 5:
            jump = True
        elif self.vel.y < 0:
            jump = False

        if self.pos.y > 1000:
            pygame.quit()

        self.rect.midbottom = self.pos

    def update(self):
        global pass_through_check
        hits = pygame.sprite.spritecollide(P1, platform_group, False)
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
    def __init__(self, x2, y2):
        pygame.sprite.Sprite.__init__(self)
        self.image = plat_img
        self.rect = self.image.get_rect()
        self.rect.x = x2
        self.rect.y = y2



platform_group = pygame.sprite.Group()

for p in range(MAX_PLATFORMS):
    p_w = random.randint(40, 60)
    p_x = random.randint(0, width - p_w)
    p_y = p * random.randint(80, 120)
    platformp = Platform(p_x, p_y)
    platform_group.add(platformp)

P1 = Player()


all_sprites = pygame.sprite.Group()
all_sprites.add(P1)


while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            sys.exit()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    platform_group.draw(screen)
    P1.move()
    P1.update()

    pygame.draw.line(screen, "white", (0, SCROLL_THRESH), (width, SCROLL_THRESH))

    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
