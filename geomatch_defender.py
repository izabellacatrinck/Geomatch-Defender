import pygame
import sys
import random
from pygame.locals import *

pygame.init()

# const
S_WIDTH = 700
S_HEIGHT = 700
BG = (0, 0, 0)
FPS = 60

# creating screen
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption('Geomatch Defender')

# classe do paddle ainda com as funções mais básicas
class PADDLE:
    direction = None

    # função de início
    def __init__(self, x, y, width, height, VELOCIDADE=6, TIRO_VELOCIDADE=230):
        self.VELOCIDADE = VELOCIDADE
        self.TIRO_VELOCIDADE = TIRO_VELOCIDADE
        self.width = width
        self.height = height
        self.screen_width = S_WIDTH
        self.screen_height = S_HEIGHT
        self.x = (S_WIDTH - self.width) // 2
        self.y = S_HEIGHT - self.height - 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0
        self.shots = []

    def move(self, dt):
        self.direction = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.x -= self.VELOCIDADE
            self.direction = -1
        if keys[pygame.K_RIGHT] and self.rect.right < S_WIDTH:
            self.x += self.VELOCIDADE
            self.direction = 1
        self.rect.x = self.x

    # função para desenhar o paddle inicialmente como um triângulo
    def draw(self, screen):
        vertices = [(self.x + self.width // 2, self.y),
                    (self.x, self.y + self.height),
                    (self.x + self.width, self.y + self.height)]
        color = (255, 0, 0)
        pygame.draw.polygon(screen, color, vertices)

    # mecânica de tiro
    def throw(self):
        new_throw = {'x': self.x + self.width // 2, 'y': self.y,
                     'rect': pygame.Rect(self.x + self.width // 2, self.y, 5, 10)}
        self.shots.append(new_throw)

    def move_shots(self, dt):
        for shot in self.shots:
            shot['y'] -= self.TIRO_VELOCIDADE * dt

    def draw_shots(self, screen):
        for shot in self.shots:
            pygame.draw.rect(screen, (255, 255, 255), (shot['x'], shot['y'], 5, 10))

    def check_collision_paddle(self, shapes):
        for shape in shapes:
            if self.rect.colliderect(pygame.Rect(shape.x - 20, shape.y - 20, 40, 40)):
                return True
        return False

class Shape:
    def __init__(self, x, y, shape_type, speed):
        self.x = x
        self.y = y
        self.shape_type = shape_type
        self.speed = speed

    def move(self, dt):
        self.y += self.speed * dt

    def draw(self, screen):
        if self.shape_type == "circle":
            pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 20)
        elif self.shape_type == "square":
            pygame.draw.rect(screen, (0, 0, 255), (int(self.x) - 20, int(self.y) - 20, 40, 40))

def check_collision(shots, shapes):
    for shot in shots:
        shot_rect = pygame.Rect(shot['x'], shot['y'], 5, 10)
        for shape in shapes:
            if pygame.Rect(shape.x - 20, shape.y - 20, 40, 40).colliderect(shot_rect):
                shapes.remove(shape)
                shots.remove(shot)
    return False

shapes = []
next_spawn_time = pygame.time.get_ticks() + 2000 # primeira queda

paddle = PADDLE(0, 0, 50, 50)
clock = pygame.time.Clock()

# GAME LOOP
while True:
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paddle.throw()

    screen.fill(BG)
    paddle.draw(screen)
    paddle.move(dt)
    paddle.draw_shots(screen)
    paddle.move_shots(dt)

    current_time = pygame.time.get_ticks()

    if current_time >= next_spawn_time:
        x = random.randint(0, S_WIDTH)
        y = 0
        shape_type = random.choice(["circle", "square"])
        speed = random.randint(50, 150) 
        shapes.append(Shape(x, y, shape_type, speed))
        next_spawn_time = current_time + 1000 # velocidade de queda após a primeira

    for shape in shapes:
        shape.move(dt)
        shape.draw(screen)

    if check_collision(paddle.shots, shapes):
        print("Collision with player!")
        pygame.quit()
        sys.exit()

    if paddle.check_collision_paddle(shapes):
        print("Collision with player!")
        pygame.quit()
        sys.exit()

    pygame.display.flip()
