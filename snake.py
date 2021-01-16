import sys
from time import sleep
import pygame
from random import randrange

# Window

WINDOW_HEIGHT = 480
WINDOW_WIDTH = 640

SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
FONT_COLOR = (255, 255, 255)

DIFFICULTY = {
    'easy': 10,
    'medium': 25,
    'hard': 40
}


class Game:
    def __init__(self):
        """
        Init class variables for game
        """
        self.game = pygame
        self.game.init()
        self.game.display.set_caption('Snake')
        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = Score()
        self.window = Window(self.game.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT)))

    def game_over(self):
        # 1 Head outside of the screen
        if self.snake.snake_head[0] < 0 or self.snake.snake_head[0] > WINDOW_WIDTH - 10:
            self.window.draw_game_over(self.game, self.exit_game)
        elif self.snake.snake_head[1] < 0 or self.snake.snake_head[1] > WINDOW_HEIGHT - 10:
            self.window.draw_game_over(self.game, self.exit_game)
        # 2 Snake crushed its body
        for block in self.snake.snake_body[1:]:
            if block[0] == self.snake.snake_head[0] and block[1] == self.snake.snake_head[1]:
                self.window.draw_game_over(self.game, self.exit_game)

    def exit_game(self):
        self.game.quit()
        sys.exit()

    def turn(self):
        self.snake.snake_move()
        if self.snake.snake_head[0] == self.food.food[0] and self.snake.snake_head[1] == self.food.food[1]:
            self.snake.snake_grown()
            self.food.food_respawn()
            self.score.increase_score()

    def run(self):
        while True:
            for event in self.game.event.get():
                if event.type == self.game.QUIT:
                    self.exit_game()
                elif event.type == self.game.KEYDOWN:
                    if event.key == self.game.K_ESCAPE:
                        self.exit_game()
                    else:
                        if event.key == self.game.K_DOWN or event.key == self.game.K_s:
                            self.snake.snake_change_direction('DOWN')
                        if event.key == self.game.K_UP or event.key == self.game.K_w:
                            self.snake.snake_change_direction('UP')
                        if event.key == self.game.K_LEFT or event.key == self.game.K_a:
                            self.snake.snake_change_direction('LEFT')
                        if event.key == self.game.K_RIGHT or event.key == self.game.K_d:
                            self.snake.snake_change_direction('RIGHT')
            self.turn()
            self.game_over()
            self.window.draw_stage()
            self.window.draw_snake(self.game, self.snake.snake_body)
            self.window.draw_food(self.game, self.food.food)
            self.window.draw_score(self.game, self.score.score)
            self.game.display.update()
            self.fps.tick(DIFFICULTY['easy'])


class Snake:
    def __init__(self):
        self.snake_direction = 'RIGHT'
        self.snake_head = [100, 50]
        self.snake_body = [
            self.snake_head,
            [self.snake_head[0] - 10, self.snake_head[1]],
            [self.snake_head[0] - 20, self.snake_head[1]],
        ]

    def snake_change_direction(self, new_snake_direction: str):
        if new_snake_direction == self.snake_direction:
            return
        if self.snake_direction == 'UP' and new_snake_direction == 'DOWN':
            return
        if self.snake_direction == 'DOWN' and new_snake_direction == 'UP':
            return
        if self.snake_direction == 'LEFT' and new_snake_direction == 'RIGHT':
            return
        if self.snake_direction == 'RIGHT' and new_snake_direction == 'LEFT':
            return
        self.snake_direction = new_snake_direction

    def snake_move(self):
        if self.snake_direction == 'UP':
            self.snake_head = [self.snake_head[0], self.snake_head[1] - 10]
        elif self.snake_direction == 'DOWN':
            self.snake_head = [self.snake_head[0], self.snake_head[1] + 10]
        elif self.snake_direction == 'RIGHT':
            self.snake_head = [self.snake_head[0] + 10, self.snake_head[1]]
        elif self.snake_direction == 'LEFT':
            self.snake_head = [self.snake_head[0] - 10, self.snake_head[1]]
        self.snake_body.insert(0, self.snake_head)
        self.snake_body.pop()

    def snake_grown(self):
        self.snake_body.insert(0, self.snake_head)
        self.snake_move()


class Food:
    def __init__(self):
        self.food = [200, 200]

    def food_respawn(self):
        self.food = [randrange(1, WINDOW_WIDTH // 10) * 10, randrange(1, WINDOW_HEIGHT // 10) * 10]


class Score:
    def __init__(self):
        self.score = 0

    def increase_score(self):
        self.score += 10


class Window:
    def __init__(self, window):
        self.window = window

    def draw_stage(self):
        self.window.fill(BACKGROUND_COLOR)

    def draw_snake(self, game, snake_body):
        for part in snake_body:
            game.draw.rect(self.window, SNAKE_COLOR, game.Rect(part[0], part[1], 10, 10))

    def draw_food(self, game, food):
        game.draw.rect(self.window, FOOD_COLOR, game.Rect(food[0], food[1], 10, 10))

    def draw_score(self, game, score):
        SCORE_FONT = game.font.SysFont('Times New Roman', 20)
        score_surface = SCORE_FONT.render(f'Score: {score}', True, FONT_COLOR)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (WINDOW_WIDTH // 2, 15)
        self.window.blit(score_surface, score_rect)

    def draw_game_over(self, game, exit_game):
        SCORE_FONT = game.font.SysFont('Times New Roman', 60)
        score_surface = SCORE_FONT.render(f'GAME OVER', True, FOOD_COLOR)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
        self.window.fill(BACKGROUND_COLOR)
        self.window.blit(score_surface, score_rect)
        game.display.update()
        sleep(3)
        exit_game()


