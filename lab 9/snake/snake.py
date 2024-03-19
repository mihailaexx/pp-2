# import pygame, random

# player_w, player_h = (1000, 900)
# screen = pygame.display.set_mode((player_w, player_h))
# pygame.init()

# screen_net = pygame.Surface((player_w, player_h), pygame.SRCALPHA)
# for i in range(1,20):
#     pygame.draw.line(screen_net, (0,0,0,130), (0, i*50), (1000, i*50))
#     pygame.draw.line(screen_net, (0,0,0,130), (i*50, 0), (i*50, 900))

# apple_time = pygame.USEREVENT + 1

# done = False

# def crete_entity():
#     return (random.randint(1,18)*50+25, random.randint(1,16)*50+25)

# class Snake():
#     def __init__(self) -> None:
#         self.x, self.y = crete_entity()
#         self.part_radius = 25
#         self.color = (0,100,0)
#         self.parts = [(self.x, self.y)]
#         self.direction = None
#         self.speed = 2
#         self.game_over = 0
#         self.score = 0
#     def drawing(self):
#         for part in self.parts:
#             pygame.draw.circle(screen, self.color, part, self.part_radius)
#     def moving(self):
#         if self.direction == "up": self.y -= self.speed * 25
#         elif self.direction == "down": self.y += self.speed * 25
#         elif self.direction == "left": self.x -= self.speed * 25
#         elif self.direction == "right": self.x += self.speed * 25
#         for i in range(len(self.parts) - 1, 0, -1):
#             self.parts[i] = self.parts[i - 1]
#         if self.parts:
#             self.parts[0] = (self.x,self.y)
#     def collision(self):
#         if (self.x, self.y) in self.parts and len(self.parts) != 1:
#             return 1
#         if self.x < self.part_radius or self.x > player_w - self.part_radius or self.y < self.part_radius or self.y > player_h - self.part_radius:
#             return 1
#         return 0

# class Apple():
#     def __init__(self) -> None:
#         self.color = (230,0,0)
#         self.pos = crete_entity()
#     def drawing(self):
#         pygame.draw.circle(screen, self.color, self.pos, 25)
#     def new_pos(self, snake):
#         if (snake.x, snake.y) == self.pos:
#             snake.parts.append(self.pos)
#             self.pos = crete_entity()
#             while self.pos in snake.parts:
#                 self.pos = crete_entity()
#             snake.score += 1

# snake = Snake()
# apple = Apple()
# while not done:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = 1
#         # if event.type == apple_time:
#         #     apple.new_pos()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and snake.direction != "down":
#                 snake.direction = "up"
#             elif event.key == pygame.K_DOWN and snake.direction != "up":
#                 snake.direction = "down"
#             elif event.key == pygame.K_LEFT and snake.direction != "right":
#                 snake.direction = "left"
#             elif event.key == pygame.K_RIGHT and snake.direction != "left":
#                 snake.direction = "right"
    
#     screen.fill((255, 255, 255))
#     screen.blit(screen_net, (0,0))
#     apple.drawing()
#     apple.new_pos(snake)
#     snake.drawing()
#     snake.moving()
    
    
#     if snake.collision():
#         done = 1
#     pygame.display.flip()
#     pygame.time.Clock().tick(snake.speed)

import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0, 130)
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
RED = (230, 0, 0)

# Game settings
SIZE = (1000, 900)
SNAKE_PART_RADIUS = 25
SNAKE_PART_DIAMETER = 2 * SNAKE_PART_RADIUS
FPS = 60

# Define classes
class Apple:
    def __init__(self):
        self.position = self.create_entity()
        self.weight = random.randint(1, 3)

    def create_entity(self):
        return (random.randint(1, 18) * 50 + 25, random.randint(1, 16) * 50 + 25)

    def draw(self, screen):
        weight_text = game.font.render(str(self.weight), True, BLACK)
        weight_text_rect = weight_text.get_rect(center=self.position)
        pygame.draw.circle(screen, RED, self.position, SNAKE_PART_RADIUS-10 + self.weight*2.5)
        screen.blit(weight_text, weight_text_rect)

class Snake:
    def __init__(self):
        self.parts = [self.create_entity()]
        self.direction = None
        self.grow_next = False

    def create_entity(self):
        return (random.randint(1, 18) * 50 + 25, random.randint(1, 16) * 50 + 25)

    def move(self):
        if self.direction:
            x, y = self.parts[0]
            if self.direction == pygame.K_UP:
                y -= SNAKE_PART_DIAMETER
            elif self.direction == pygame.K_DOWN:
                y += SNAKE_PART_DIAMETER
            elif self.direction == pygame.K_LEFT:
                x -= SNAKE_PART_DIAMETER
            elif self.direction == pygame.K_RIGHT:
                x += SNAKE_PART_DIAMETER

            new_head = (x, y)
            
            if self.grow_next:
                # Add the new head without removing the last part
                self.parts = [new_head] + self.parts
                self.grow_next = False
            else:
                # Add the new head and remove the last part to simulate movement
                self.parts = [new_head] + self.parts[:-1]

    def draw(self, screen):
        for part in self.parts:
            pygame.draw.circle(screen, GREEN, part, SNAKE_PART_RADIUS)

    def grow(self):
        self.grow_next = True  # Mark to grow in the next move

    def check_collision(self):
        return self.parts[0] in self.parts[1:]

    def check_boundary(self):
        x, y = self.parts[0]
        if self.parts[0][0] < SNAKE_PART_RADIUS or x > SIZE[0] - SNAKE_PART_RADIUS or y < SNAKE_PART_RADIUS or y > SIZE[1] - SNAKE_PART_RADIUS:
            return True

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE)
        self.snake = Snake()
        self.apple = Apple()
        self.score = 0
        self.level = 0
        self.font = pygame.font.Font(None, 24)
        self.go_font = pygame.font.Font(None, 128)
        self.clock = pygame.time.Clock()
        self.done = False
        self.game_over = False
        self.draw_background()

    def draw_background(self):
        self.screen.fill(WHITE)
        for i in range(1, 20):
            pygame.draw.line(self.screen, BLACK, (0, i * 50), (1000, i * 50))
            pygame.draw.line(self.screen, BLACK, (i * 50, 0), (i * 50, 900))

    def run(self):
        while not self.done:
            self.handle_events()
            if not self.game_over:
                self.update_game()
            self.draw_game()
            self.clock.tick(FPS)
            if not self.game_over:
                pygame.time.delay(self.calculate_speed_delay())

    def calculate_speed_delay(self):
        delay = max(1000 - (self.score * 25), 250)
        return delay
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            # elif event.type in (pygame.KEYDOWN, pygame.KEYUP) and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            #     self.snake.direction = event.key
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and self.snake.direction != pygame.K_DOWN:
                    self.snake.direction = pygame.K_UP
                elif event.key == pygame.K_DOWN and self.snake.direction != pygame.K_UP:
                    self.snake.direction = pygame.K_DOWN
                elif event.key == pygame.K_LEFT and self.snake.direction != pygame.K_RIGHT:
                    self.snake.direction = pygame.K_LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != pygame.K_LEFT:
                    self.snake.direction = pygame.K_RIGHT

    def update_game(self):
        self.snake.move()
        if self.snake.parts[0] == self.apple.position:
            self.score += self.apple.weight
            self.apple = Apple()
            self.snake.grow()
        if self.snake.check_collision() or self.snake.check_boundary():
            self.game_over = True
        self.level = self.score // 2

    def draw_game(self):
        self.draw_background()
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        level_text = self.font.render(f"Level: {self.level}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 30))
        if self.game_over:
            self.show_game_over()
        pygame.display.flip()

    def show_game_over(self):
        game_over_text = self.go_font.render("GAME OVER", True, RED, (12, 12, 12))
        self.screen.blit(game_over_text, (250, 300))
        pygame.display.flip()
        time.sleep(2)
        self.done = True

if __name__ == "__main__":
    game = Game()
    game.run()
