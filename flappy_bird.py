import pygame
import random
import sys

pygame.init()

# Constants
WIDTH = 400
HEIGHT = 600
GROUND = HEIGHT - 70
FPS = 30
BIRD_JUMP = -10
GRAVITY = 1
PIPE_VELOCITY = -5
PIPE_GAP = 150
PIPE_FREQUENCY = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.img = pygame.image.load("bird.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (50, 50))
        self.rect = self.img.get_rect()

    def jump(self):
        self.velocity = BIRD_JUMP

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.img, self.rect)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.img_top = pygame.image.load("pipe_top.png").convert_alpha()
        self.img_top = pygame.transform.scale(self.img_top, (50, self.height))
        self.img_bottom = pygame.image.load("pipe_bottom.png").convert_alpha()
        self.img_bottom = pygame.transform.scale(self.img_bottom, (50, HEIGHT - self.height - PIPE_GAP))
        self.rect_top = self.img_top.get_rect()
        self.rect_bottom = self.img_bottom.get_rect()

    def update(self):
        self.x += PIPE_VELOCITY
        self.rect_top = self.img_top.get_rect(topleft=(self.x, 0))
        self.rect_bottom = self.img_bottom.get_rect(topleft=(self.x, self.height + PIPE_GAP))

    def draw(self, screen):
        screen.blit(self.img_top, self.rect_top)
        screen.blit(self.img_bottom, self.rect_bottom)

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
bird = Bird()
pipes = []

# Load images
background_img = pygame.image.load("background.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
ground_img = pygame.image.load("ground.png").convert()
ground_img = pygame.transform.scale(ground_img, (WIDTH, 70))

# Game loop
running = True
while running:
    screen.blit(background_img, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    # Bird
    bird.update()
    bird.draw(screen)

    # Pipes
    if len(pipes) == 0 or pipes[-1].x < WIDTH - PIPE_FREQUENCY:
        pipes.append(Pipe(WIDTH))
    for pipe in pipes:
        pipe.update()
        pipe.draw(screen)
        if pipe.rect_top.colliderect(bird.rect) or pipe.rect_bottom.colliderect(bird.rect) or bird.rect.bottom >= GROUND:
            running = False
        if pipe.x < -50:
            pipes.remove(pipe)

    # Ground
    screen.blit(ground_img, (0, GROUND))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
