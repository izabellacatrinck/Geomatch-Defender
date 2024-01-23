import pygame
import sys
import random

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font('PressStart2P.ttf', 40)
press_enter_font = pygame.font.Font('PressStart2P.ttf', 25)

# const
S_WIDTH = 700
S_HEIGHT = 700
BG = (0, 0, 0)
FPS = 60
score = 0
disharmony_count = 0
shape_counter = 0
WHITE = (255, 255, 255)

#efeitos sonoros
lazer_sound = pygame.mixer.Sound('8-Bit Laser Gun Sound Effect (cut.).mp3')
impact_sound = pygame.mixer.Sound('8 bit impact sound effect (volume up).mp3')
sound_track = pygame.mixer.Sound('geomatch_soundtrack.mp3')
game_over_sound = pygame.mixer.Sound('game over - sound effect.mp3')
# creating screen
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption('Geomatch Defender')
sound_track.play()

fundo = pygame.image.load('Imagem_menu_Geomath.png')
screen.blit(fundo, (0, 0))
class main_menu:

    loop = True
    while loop:
        press_enter_text = press_enter_font.render(f'Press the enter key to play', True, WHITE)
        press_enter_text_rect = press_enter_text.get_rect(center=(S_WIDTH // 2, S_HEIGHT // 1.4))
        screen.blit(press_enter_text, press_enter_text_rect)
        pygame.display.flip()
        for events in pygame.event.get():
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_KP_ENTER or events.key == pygame.K_RETURN:
                    is_pressing_enter = True
                    loop = False
        pygame.display.update()
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

    # função para desenhar o paddle
    def draw(self, screen, shape_type_paddle):
        if shape_type_paddle == 0:
            vertices = [(self.x + self.width // 2, self.y),
                        (self.x, self.y + self.height),
                        (self.x + self.width, self.y + self.height)]
            color = (255, 0, 0)
            pygame.draw.polygon(screen, color, vertices)
        elif shape_type_paddle == 1:
            pygame.draw.circle(screen, (255, 255, 0), (int(self.x) + 28, int(self.y) + 28), 20)
        elif shape_type_paddle == 2:
            pygame.draw.rect(screen, (0, 0, 255), (int(self.x) + 8, int(self.y) + 8, 40, 40))

    # Função usada para determinar o tipo de paddle
    def change(self):
        global shape_counter
        shape_counter += 1
        if shape_counter == 3:
            shape_counter = 0

    # mecânica de tiro
    def throw(self):
        if shape_counter == 0:
            new_throw = {'x': self.x + self.width // 2, 'y': self.y,
                        'rect': pygame.Rect(self.x + self.width // 2, self.y, 5, 10),
                        'shot_from': "triangle"}
            self.shots.append(new_throw)
        elif shape_counter == 1:
            new_throw = {'x': self.x + self.width // 2, 'y': self.y,
                         'rect': pygame.Rect(self.x + self.width // 2, self.y, 5, 10),
                         'shot_from': "circle"}
            self.shots.append(new_throw)
        elif shape_counter == 2:
            new_throw = {'x': self.x + self.width // 2, 'y': self.y,
                         'rect': pygame.Rect(self.x + self.width // 2, self.y, 5, 10),
                         'shot_from': "square"}
            self.shots.append(new_throw)
        lazer_sound.play()


    def move_shots(self, dt):
        for shot in self.shots:
            shot['y'] -= self.TIRO_VELOCIDADE * dt

    def draw_shots(self, screen):
        for shot in self.shots:
            pygame.draw.rect(screen, (255, 255, 255), (shot['x'], shot['y'], 5, 10))

    def check_collision_paddle(self, shapes):
        collision_shapes = []
        for shape in shapes:
            if self.rect.colliderect(pygame.Rect(shape.x - 20, shape.y - 20, 40, 40)):
                collision_shapes.append(shape)
        return collision_shapes


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
        elif self.shape_type == "triangle":
            vertices = [(self.x + 50 // 2, self.y),
                        (self.x, self.y + 50),
                        (self.x + 50, self.y + 50)]
            pygame.draw.polygon(screen, (255, 0, 0), vertices)


def check_collision(shots, shapes):
    global score, disharmony_count
    for shot in shots:
        shot_rect = pygame.Rect(shot['x'], shot['y'], 5, 10)
        for shape in shapes:
            if pygame.Rect(shape.x - 20, shape.y - 20, 40, 40).colliderect(shot_rect):
                shapes.remove(shape)
                shots.remove(shot)
                if shot['shot_from'] != shape.shape_type:
                    if shape.shape_type == "triangle":
                        score += 5
                    elif shape.shape_type == "square":
                        score += 10
                    elif shape.shape_type == "circle":
                        score += 15
                else:
                    disharmony_count += 1


def shape_escaped(shapes):
    for shape in shapes:
        if shape.y >= S_HEIGHT:
            shapes.remove(shape)
            return True
    return False


shapes = []
next_spawn_time = pygame.time.get_ticks() + 2000  # primeira queda

paddle = PADDLE(0, 0, 50, 50)
clock = pygame.time.Clock()

# GAME LOOP
while True:
    disharmony_text = font.render(f"Disharmony: {disharmony_count}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paddle.throw()
            if event.key == pygame.K_DOWN:
                paddle.change()

    screen.fill(BG)
    screen.blit(score_text, (10, 10))
    screen.blit(disharmony_text, (S_WIDTH - disharmony_text.get_width() - 10, 10))
    paddle.draw(screen, shape_counter)
    paddle.move(dt)
    paddle.draw_shots(screen)
    paddle.move_shots(dt)
    check_collision(paddle.shots, shapes)

    current_time = pygame.time.get_ticks()

    if current_time >= next_spawn_time:
        x = random.randint(20, S_WIDTH - 50)
        y = 0
        shape_type = random.choice(["circle", "square", "triangle"])
        speed = random.randint(50, 150)
        shapes.append(Shape(x, y, shape_type, speed))
        next_spawn_time = current_time + 1000  # velocidade de queda após a primeira

    for shape in shapes:
        shape.move(dt)
        shape.draw(screen)

    # check if shape reached the bottom
    if shape_escaped(shapes):
        disharmony_count += 1

    # disharmony updates
    collision_shapes = paddle.check_collision_paddle(shapes)
    if collision_shapes:
        impact_sound.play()
        for shape in collision_shapes:
            if shape.shape_type == "triangle" and shape_counter == 0:
                score += 5
            elif shape.shape_type == "square" and shape_counter == 2:
                score += 10
            elif shape.shape_type == "circle" and shape_counter == 1:
                score += 15
            else:
                disharmony_count += 1
            shapes.remove(shape)

    # game over system
    if disharmony_count == 3:
        sound_track.stop()
        screen.fill((0, 0, 0))
        game_over_text = game_over_font.render(f'Game Over', True, WHITE)
        game_over_text_rect= game_over_text.get_rect(center=(S_WIDTH//2, S_HEIGHT//2))
        screen.blit(game_over_text, game_over_text_rect)
        pygame.display.flip()
        game_over_sound.play()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    pygame.display.flip()