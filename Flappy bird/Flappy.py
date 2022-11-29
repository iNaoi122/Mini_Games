import time

import pygame
import sys
from random import randint

# window
WIGHT = 1200
HEIGHT = 900
FPS = 60

# game const
SPEED = 15
GRAVITY = 3
JUMP = -15
COUNT_PLAYER_IMAGES = 3

# sizes
PIPE_SCALE_X = 50
PIPE_SCALE_Y = HEIGHT // 3
PLAYER_SIZE = (50, 36)
RANDOM_PIPES = (-50, 60)
DIST_BETWEEN_PIPES = 700
DIGIT_SIZE = 50

# spawn pos
PLAYER_POS = (WIGHT * 0.2, HEIGHT // 2)
GROUND_HEIGHT = HEIGHT * 0.15
TOP_PIPE_SPAWN = (WIGHT, 0)
BOTTOM_PIPE_SPAWN = (WIGHT, HEIGHT)
SCORE_POS = (WIGHT // 2, HEIGHT * 0.2)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.screen = pygame.display.set_mode((WIGHT, HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_images()
        self.score_ = Score(self.screen)
        self.all_sprite = pygame.sprite.Group()
        self.pipes_active = pygame.sprite.Group()
        self.start_game()
        self.pipe_distance = 0
        self.count = 0

    def start_game(self):
        self.player = Player(self.player_images)
        self.all_sprite.add(self.player)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.player.jump(pygame.key.get_pressed())

    def update(self):
        self.all_sprite.update()
        self.clock.tick(FPS)
        self.add_pipe()
        self.score()
        self.collision()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprite.draw(self.screen)
        self.screen.blit(self.ground, (0, HEIGHT - GROUND_HEIGHT))
        self.score_.draw()
        pygame.display.flip()

    def load_images(self):
        self.player_images = []
        [self.player_images.append(pygame.transform.scale(pygame.image.load(f"images/bird{i}.png"), PLAYER_SIZE))
         for i in range(1, COUNT_PLAYER_IMAGES + 1)]
        self.background = pygame.transform.scale(pygame.image.load("images/bg.png"), (WIGHT, HEIGHT))
        self.ground = pygame.transform.scale(pygame.image.load("images/ground.png"), (WIGHT, GROUND_HEIGHT))
        self.pipe_image = pygame.transform.scale(pygame.image.load("images/pipe.png"), (PIPE_SCALE_X, PIPE_SCALE_Y))

    def run(self):
        time.sleep(10)
        while True:
            self.check_events()
            self.update()
            self.draw()

    def add_pipe(self):
        self.pipe_distance += SPEED
        if self.pipe_distance > DIST_BETWEEN_PIPES:
            self.pipe_distance = 0

            top_pipe = TopPipe(self.pipe_image)
            bottom_pipe = BottomPipe(self.pipe_image)

            self.all_sprite.add(top_pipe)
            self.all_sprite.add(bottom_pipe)

            self.pipes_active.add(top_pipe)
            self.pipes_active.add(bottom_pipe)

    def score(self):
        for pipe in self.pipes_active:
            if self.player.rect.left > pipe.rect.left:
                self.pipes_active.remove(pipe)
                self.score_.score += 0.5

    def collision(self):
        if pygame.sprite.spritecollide(self.player, self.pipes_active, False, collided=pygame.sprite.collide_mask) or \
                self.player.rect.bottom > HEIGHT - GROUND_HEIGHT or self.player.rect.top <= 0:
            print("Game Over")
            pygame.quit()
            sys.exit()


class Player(pygame.sprite.Sprite):
    def __init__(self, player_images):
        super(Player, self).__init__()
        self.images = player_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=PLAYER_POS)
        self.index = 0

    def jump(self, keys):
        if keys[pygame.K_SPACE]:
            self.rect.move_ip(0, JUMP)

    def down(self):
        self.rect.move_ip(0, GRAVITY)

    def update_images(self):
        if self.index > COUNT_PLAYER_IMAGES - 1:
            self.index = 0
        if self.index % 1 == 0:
            self.image = self.images[int(self.index)]

        self.index += 0.5

    def update(self):
        self.down()
        self.update_images()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, pipe_image):
        super(Pipe, self).__init__()
        self.image = pygame.transform.scale(pipe_image, (PIPE_SCALE_X, PIPE_SCALE_Y + randint(*RANDOM_PIPES)))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= SPEED
        if self.rect.left < 0:
            self.kill()


class TopPipe(Pipe):
    def __init__(self, pipe_image):
        super(TopPipe, self).__init__(pipe_image)
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect.topleft = WIGHT, 0


class BottomPipe(Pipe):
    def __init__(self, pipe_image):
        super(BottomPipe, self).__init__(pipe_image)
        self.rect.bottomleft = WIGHT, HEIGHT - GROUND_HEIGHT


class Score:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", DIGIT_SIZE)
        self.score = 0

    def draw(self):
        self.text_font = self.font.render(f"{int(self.score)}", True, (255, 255, 255))
        self.screen.blit(self.text_font, SCORE_POS)


if __name__ == '__main__':
    game = Game()
    game.run()
