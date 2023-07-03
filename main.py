# Import packages
import pygame
from pygame.locals import *
import sys
import random

# constants
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
moving_plat_img = pygame.image.load("graphic/moving plat.png").convert_alpha()
bg_image = pygame.image.load("graphic/silly background.png").convert_alpha()
sprite_1 = pygame.image.load("graphic/CAT SPRITE  DARK 1.png").convert_alpha()
sprite_2 = pygame.image.load("graphic/CAT SPRITE  DARK 2.png").convert_alpha()
score_line = pygame.image.load("graphic/score background.png").convert_alpha()
spring_img = pygame.image.load("graphic/block.png").convert_alpha()
max_platforms = 13
scroll_height = 300
higher_scroll_height = 0
scroll = 0
bg_scroll = 0
time = pygame.time.get_ticks()
spring_img = pygame.Surface((20, 20))
spring_img.fill("black")
max_springs = 2
score = 0
platform_vel = 5
max_moving_platforms = 5
platform_kill = 0

# Font for text
def get_font(size):
    return pygame.font.Font("TenOClockRegular-8L7n.ttf", size)

# Spawning background image
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -920 + bg_scroll))


# Player character
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
        # Moving character left and right
        if pressed_keys[K_LEFT]:
            self.acc.x = -acceleration - 0.1
        if pressed_keys[K_RIGHT]:
            self.acc.x = acceleration + 0.1

        self.acc.x += self.vel.x * friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Player can't go out of borders
        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        if self.vel.y > 5:
            jump = True
        elif self.vel.y < 0:
            jump = False

        # Game ends if character goes beyond bottom border
        if self.pos.y > 1000:
            pygame.quit()

        self.rect.midtop = self.pos

        # Keeps character from going off the top border
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
        if scroll:
            score += 2
        text = get_font(70).render(str(score), True, "black")
        text_rect = text.get_rect()
        text_rect.center = (width // 8, height // 18)
        screen.blit(text, text_rect)

        # Collision + sprite animation
        if hits and jump == True:
            self.rect.bottom = hits[0].rect.top + 1
            self.vel.y = 0
            P1.jump()
            self.surf = sprite_2
            time = 0
        elif self.vel.y > 1:
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
        screen.blit(self.spot_light, (self.pos.x - 180, self.pos.y - 160))


class Platform(pygame.sprite.Sprite):
    def __init__(self, x2, y2):
        pygame.sprite.Sprite.__init__(self)
        self.image = plat_img
        self.rect = self.image.get_rect()
        self.rect.x = x2
        self.rect.y = y2

    def update(self, scroll):
        global platform_kill
        self.rect.y += scroll

        if self.rect.top > height:
            self.kill()
            platform_kill += 1


class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x2, y2, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = moving_plat_img
        self.rect = self.image.get_rect()
        self.rect.x = x2
        self.rect.y = y2
        self.speed = speed

    def update(self, scroll):
        global platform_vel
        global platform_kill

        self.rect.y += scroll
        self.rect.x += self.speed

        if self.rect.top > height:
            self.kill()
            platform_kill += 1

        if self.rect.x > width:
            self.rect.x = -150
        if self.rect.x < -150:
            self.rect.x = width


class Object:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window):
        pygame.draw.rect(window, (0, 255, 0), self.rect)

    def collide(self, other_rect):
        return self.rect.colliderect(other_rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def collide(self, other_rect):
        return self.rect.colliderect(other_rect)


platform_group = pygame.sprite.Group()

platform = Platform(width // 2 - 50, height - 50)
platform_group.add(platform)

objects = []
moving_platforms = []

P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)

top_plat = platform.rect.midtop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            sys.exit()

    # Scrolls background
    bg_scroll += scroll
    if bg_scroll >= height:
        bg_scroll = 0
    draw_bg(bg_scroll)
    time += 1
    platform_group.update(scroll)

    # Randomly spawns platforms
    if len(platform_group) < max_platforms:
        p_x = random.randint(0, 500)
        p_y = platform.rect.y - random.randint(80, 200)
        platform = Platform(p_x, p_y)
        platform_group.add(platform)

    # Randomly spawns moving platform after conditions are met
    if random.randint(0, 100) < 0.1 and len(moving_platforms) < 3:
        moving_platform_x = random.randint(50, 200)
        moving_platform_y = random.randint(-400, 0)
        moving_platform_speed = random.choice([-2, -1, 1, 2])

        moving_platform = MovingPlatform(moving_platform_x, moving_platform_y, moving_platform_speed)
        platform_group.add(moving_platform)

        # Randomly spawns objects on moving platform
        object_width = 30
        object_height = 30
        object_x = moving_platform_x + random.randint(0, 100 - object_width)
        object_y = moving_platform_y - object_height
        object_instance = Object(object_x, object_y, object_width, object_height)
        objects.append(object_instance)

    for moving_platform in moving_platforms:
        moving_platform.update()
        moving_platform.draw(screen)

    for object_instance in objects:
        object_instance.draw(screen)
        object_instance.move(0, 0)

    # Collision for the objects
    for moving_platform in moving_platforms:
        for object_instance in objects:
            if object_instance.collide(platform.rect):
                # Collision detected between object and platform
                # Handle the collision logic here
                pass

    platform_group.draw(screen)
    P1.light_effect()
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    screen.blit(score_line, (0, 0))
    P1.move()
    P1.update()
    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
