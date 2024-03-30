import pygame 
import random
pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60
BLACK = (0, 0, 0)

done = 0

class Paddle():
    def __init__(self, w, h, color: tuple = (255, 255, 255)):
        self.w = w
        self.h = h
        self.padding_bottom = 10
        self.speed = 20
        self.rect = pygame.Rect(WIDTH // 2 - self.w // 2, HEIGHT - self.h - self.padding_bottom, self.w, self.h)
        self.color = color
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Ball():
    def __init__(self, radius, color: tuple = (255, 255, 255)):
        self.radius = radius
        self.dx = random.choice([1, -1])
        self.dy = -1
        self.speed = 6
        self.rect = int(self.radius * 2 ** 0.5)
        self.ball = pygame.Rect(WIDTH // 2 - self.rect // 2, HEIGHT - self.rect - 50, self.rect, self.rect)
        self.color = color
        self.score = 0
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.ball.center, self.radius)
    def detect_collision(self, dx, dy, rect):
        if dx > 0:
            delta_x = self.ball.right - rect.left
        else:
            delta_x = rect.right - self.ball.left
        if dy > 0:
            delta_y = self.ball.bottom - rect.top
        else:
            delta_y = rect.bottom - self.ball.top

        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        if delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy
    def collision_left(self):
        if self.ball.centerx < self.radius or self.ball.centerx > WIDTH - self.radius:
            self.dx = -self.dx
    def collision_top(self):
        if self.ball.centery < self.radius: 
            self.dy = -self.dy
    def collision_paddle(self, paddle):
        if self.ball.colliderect(paddle) and self.dy > 0:
            self.dx, self.dy = self.detect_collision(self.dx, self.dy, paddle.rect)
            #* if ball hits paddle, it will move down and up by 5 pixels
            paddle.rect.y += 5
            def return_paddle():
                paddle.rect.y -= 5
            pygame.time.set_timer(pygame.USEREVENT, 50)
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    return_paddle()
                    pygame.time.set_timer(pygame.USEREVENT, 0)
    def collision_blocks(self, blocks, paddle):
        hitIndex = self.ball.collidelist(blocks.block_list)
        if hitIndex != -1:
            hitRect = blocks.block_list[hitIndex]
            self.dx, self.dy = self.detect_collision(self.dx, self.dy, hitRect)
            self.color = blocks.color_list[hitIndex]

            if hitRect in blocks.unbreakable_list:
                return

            if hitRect in blocks.superblocks_list:
                paddle.w += 50
                paddle.rect.width = paddle.w
            
            blocks.block_list.pop(hitIndex)
            blocks.color_list.pop(hitIndex)
            self.score += 1
            self.speed += 0.1
    def move(self):
        self.ball.x += self.speed * self.dx
        self.ball.y += self.speed * self.dy


class Blocks:
    def __init__(self, area_width, are_height, padding, n_colums=10, n_rows=4, n_unbreakable=5, n_superblocks=2):
        self.area_width = area_width
        self.area_height = are_height
        self.padding = padding
        self.width = self.calculate_block_width(area_width, n_colums, padding)
        self.height = self.calculate_block_height(are_height, n_rows, padding)
        self.block_list = [pygame.Rect(self.padding + (self.width + self.padding) * i,
                                       self.padding + (self.height + self.padding) * j, self.width, self.height)
                           for i in range(n_colums) for j in range(n_rows)]
        self.color_list = [(random.randrange(0, 255),
                            random.randrange(0, 255),  
                            random.randrange(0, 255))
                           for _ in range(n_colums*n_rows)]
        self.unbreakable_list = random.sample(self.block_list, n_unbreakable)
        self.superblocks_list = random.sample(self.block_list, n_superblocks)
    @staticmethod
    def calculate_block_width(window_width, num_blocks, padding):
        total_margin = padding * (num_blocks + 1)
        total_blocks_width = window_width - total_margin
        block_width = total_blocks_width / num_blocks
        return block_width
    @staticmethod
    def calculate_block_height(window_height, num_blocks, padding):
        total_margin = padding * (num_blocks + 1)
        total_blocks_height = window_height - total_margin
        block_height = total_blocks_height / num_blocks
        return block_height
    def draw_blocks(self, screen):
        pygame.draw.rect(screen, (255,0,0), (0, 0, self.area_width, self.area_height), 2) #* draw area for blocks
        for index, block in enumerate(self.block_list): 
            pygame.draw.rect(screen, self.color_list[index], block)
            if block in self.unbreakable_list: #* draw unbreakable blocks
                pygame.draw.rect(screen, (255,255,255), block, 4)
            if block in self.superblocks_list: #* draw super blocks with text
                pygame.draw.rect(screen, (255,255,255), block, 4)
                megablock_text = pygame.font.SysFont('comicsansms', 18).render('megablock', True, (255, 255, 255))
                text_rect = megablock_text.get_rect(center=block.center)
                screen.blit(megablock_text, text_rect)
    
class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.game_reset()
    def game_reset(self):
        self.paddle = Paddle(150, 25)
        self.ball = Ball(20)
        self.blocks = Blocks(WIDTH, HEIGHT-400, padding=20, n_colums=10, n_rows=4)
        self.started = False
        self.is_game_over = False
    def show_game_over(self):
        font = pygame.font.SysFont('comicsansms', 40)
        losetext = font.render('Game Over', True, (255, 255, 255))
        wintext = font.render('You win yay', True, (0, 0, 0))
        
        if self.ball.ball.bottom > HEIGHT:
            self.screen.fill((0, 0, 0))
            self.screen.blit(losetext, losetext.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.flip()
            self.is_game_over = True
        elif not len(self.blocks.block_list)-len(self.blocks.unbreakable_list): # list of blocks is empty
            self.screen.fill((255,255, 255))
            self.screen.blit(wintext, wintext.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.flip()
            self.is_game_over = True
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.USEREVENT:
                self.paddle.rect.y -= 5
                pygame.time.set_timer(pygame.USEREVENT, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #* start game by pressing space
                    self.paddle.rect.y -= 5
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    self.started = True
                if self.is_game_over and event.key == pygame.K_RETURN: #* restart game by pressing enter if game is over
                    self.game_reset()
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.paddle.rect.left > 0:
            self.paddle.rect.left -= self.paddle.speed
            if not self.started:
                self.ball.ball.left -= self.paddle.speed
        if key[pygame.K_RIGHT] and self.paddle.rect.right < WIDTH:
            self.paddle.rect.right += self.paddle.speed
            if not self.started:
                self.ball.ball.right += self.paddle.speed
    def update_game(self):
        self.ball.collision_left()
        self.ball.collision_top()
        self.ball.collision_paddle(self.paddle)
        self.ball.collision_blocks(self.blocks, self.paddle)
        if self.started: self.ball.move()
        self.show_game_over()
    def draw_game(self):
        self.screen.fill(BLACK)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.blocks.draw_blocks(self.screen)
        text = pygame.font.SysFont('comicsansms', 40).render(f'Your game score is: {self.ball.score}', True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=(210, 20)))
    def run(self):
        while True:
            self.handle_events()
            if not self.is_game_over:
                self.update_game()
                self.draw_game()
                self.show_game_over()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()