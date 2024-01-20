import pygame
import sys
from pygame.cursors import *
from pygame.locals import Rect
from pygame.locals import *

pygame.init()

#const
S_WIDTH = 700
S_HEIGHT = 700
BG = (0, 0, 0)
FPS = 60

# creating screen
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption('Geomatch Defender')

#classe do paddle ainda com as funções mais básicas
class PADDLE:
    direction = None

    #função de início
    def __init__(self, x, y, width, height, VELOCIDADE=10):
        self.VELOCIDADE = 10
        self.width = width
        self.height = height
        self.speed = VELOCIDADE
        self.screen_width = S_WIDTH
        self.screen_height = S_HEIGHT
        self.x = (S_WIDTH - self.width) // 2
        self.y = S_HEIGHT - self.height - 10
        self.direction = 0

    def move(self):
        self.direction = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.x -= self.VELOCIDADE
            self.direction = -1
        if keys[pygame.K_d] and self.rect.right < S_WIDTH:
            self.x += self.VELOCIDADE
            self.direction = 1
        self.rect.x = self.x

    #função para desenhar o paddle inicialmente como um triângulo
    def draw(self, screen):
        vertices = [(self.x + self.width // 2, self.y),
                    (self.x, self.y + self.height),
                    (self.x + self.width, self.y + self.height)]
        color = (255, 0 ,0)
        pygame.draw.polygon(screen, color, vertices)

paddle = PADDLE(0, 0, 50, 50)

#GAME LOOP
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG)
    paddle.draw(screen)
    pygame.display.flip()
