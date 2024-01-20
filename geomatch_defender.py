import pygame

pygame.init()

#const
S_WIDTH = 700
S_HEIGHT = 700
BG = (0, 0, 0)
FPS = 60

# creating screen
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption('Geomatch Defender')
class PADDLE:
    direction = None

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
        self.rect = Rect(self.x, self.y, self.width, self.height)

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
