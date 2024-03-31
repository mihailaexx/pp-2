import pygame
import random
from pygame.locals import *

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 600, 900
SPEED = 5

# Загрузка изображений (пример)
# Убедитесь, что у вас есть эти изображения в указанных путях или обновите пути
enemy_img_path = "lab 8/race/Enemy.png"
main_car_img_path = "lab 8/race/Car.png"
coin_img_path = "lab 8/race/Coin.png"

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_file, start_pos, screen):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect(center=start_pos)
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect)

class Enemy(GameObject):
    def update(self):
        self.cars_passed = 0
        self.rect.y += SPEED
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(0, WIDTH), -200)
            self.cars_passed += 1  # Увеличиваем счетчик пропущенных автомобилей

class MainCar(GameObject):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0: self.rect.x -= 20
        if keys[K_RIGHT] and self.rect.right < WIDTH: self.rect.x += 20
        if keys[K_UP] and self.rect.top > 0: self.rect.y -= 20
        if keys[K_DOWN] and self.rect.bottom < HEIGHT: self.rect.y += 20

class Coin(GameObject):
    def __init__(self, image_file, start_pos, screen, initial_weight=1):
        super().__init__(image_file, start_pos, screen)
        self.weight = initial_weight
        self.original_image = self.image  # Сохраняем оригинальное изображение для масштабирования
        self.update_weight(self.weight)  # Инициализируем размер с учетом веса

    def update_weight(self, new_weight):
        self.weight = new_weight
        # Масштабируем изображение в соответствии с новым весом
        width = self.original_image.get_width() * self.weight
        height = self.original_image.get_height() * self.weight
        self.image = pygame.transform.scale(self.original_image, (int(width), int(height)))
        # После изменения размера изображения необходимо обновить rect, чтобы он соответствовал новым размерам
        self.rect = self.image.get_rect(center=self.rect.center)

    def collect(self, car: MainCar):
        global SPEED
        if pygame.sprite.collide_rect(car, self):
            SPEED += 1
            self.rect.center = (random.randint(25, WIDTH-25), random.randint(25, HEIGHT-25))
            self.amount += self.weight
            # Изменяем вес (и размер) монеты при каждом сборе
            new_weight = random.choice([0.5, 1, 1.5])  # Например, вес изменяется случайно
            self.update_weight(new_weight)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.go_font = pygame.font.Font(None, 128)
        self.game_reset()

    def game_reset(self):
        global SPEED  # Обновляем глобальную переменную SPEED
        SPEED = 5  # Сбрасываем скорость к начальной
        self.player = MainCar(main_car_img_path, (WIDTH / 2, HEIGHT - 100), self.screen)
        self.enemy = Enemy(enemy_img_path, (random.randint(0, WIDTH), -200), self.screen)
        self.coin = Coin(coin_img_path, (random.randint(25, WIDTH-25), random.randint(25, HEIGHT-25)), self.screen)
        self.coin.amount = 0
        self.cars_passed = 0
        self.all_sprites = pygame.sprite.Group(self.player, self.enemy, self.coin)
        self.done = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.done = True
            if event.type == KEYDOWN and event.key == K_RETURN and self.done:
                self.game_reset()

    def update_game(self):
        self.all_sprites.update()
        self.coin.collect(self.player)
        if pygame.sprite.collide_rect(self.player, self.enemy):
            self.done = True

    def draw_game(self):
        global SPEED
        self.screen.fill((255, 255, 255))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.font.render(f"Cars passed: {self.cars_passed}", True, (0, 0, 0)), (10, 10))
        self.screen.blit(self.font.render(f"Coins: {self.coin.amount}", True, (0, 0, 0)), (10, 30))
        self.screen.blit(self.font.render(f"Speed: {SPEED}", True, (0, 0, 0)), (10, 50))
        pygame.display.flip()

    def run(self):
        while not self.done:
            self.handle_events()
            self.update_game()
            self.draw_game()
            self.clock.tick(60)  # Обновляем с заданной частотой кадров
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()