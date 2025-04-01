import pygame, sys
from pygame.locals import *
import random, time

# Initializing
pygame.init()

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen & Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Enemy speed
SCORE = 0
SCORE_TO_SPEEDUP = 5  # Every N coins speed increases
collected_score = 0  # Track collected coins

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Background
background = pygame.image.load("AnimatedStreet.png")

# Screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Coin class with random weight
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 2, 3])  # coin value
        self.image = pygame.image.load("coin.png")
        # Resize image based on weight (optional visual)
        self.image = pygame.transform.scale(self.image, (20 * self.weight, 20 * self.weight))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def reset(self):
        self.weight = random.choice([1, 2, 3])
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (20 * self.weight, 20 * self.weight))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

# Initialize sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Move and draw sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Collision with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Collision with coin
    if pygame.sprite.spritecollideany(P1, coins):
        coin = pygame.sprite.spritecollideany(P1, coins)
        SCORE += coin.weight
        collected_score += coin.weight

        # Increase speed every N collected points
        if collected_score >= SCORE_TO_SPEEDUP:
            SPEED += 1
            collected_score = 0  # Reset counter

        coin.reset()  # Replace coin with a new one

    pygame.display.update()
    FramePerSec.tick(FPS)
