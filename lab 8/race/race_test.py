import pygame, random
from pygame.locals import *
from time import sleep

pygame.init()
size = (600, 900)
screen = pygame.display.set_mode(size)

# def values for cars
car_w = 100
car_h = 200
x = size[0]/2
y = size[1]-car_h/2
done = False
SPEED = 15
cars = 0
font = pygame.font.Font(None, 24) # create 2 fonts for score and endgame
go_font = pygame.font.Font(None, 128)

INC_SPEED = pygame.USEREVENT + 1 # prioritize event
pygame.time.set_timer(INC_SPEED, 1000)

class Enemy(pygame.sprite.Sprite): # use class for game objects
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("lab 8/race/Enemy.png") # upload an image
        self.rect = self.image.get_rect() # create a collision like a rectangle
        self.rect.center=(random.randint(0,size[0]),-car_h) # randomly create an enemy behind a screen top
    
    def spawn_n_move(self):
        screen.blit(self.image, self.rect) # draw an enemy
        global cars # add a score for skipped cars
        self.rect.move_ip(0,SPEED) # move an object with changing speed
        if (self.rect.bottom > size[1]+car_h): # create a new car after one go out from a screen
            self.rect.center = (random.randint(0,size[0]),-car_h)
            cars += 1 # tick a score

class MainCar(pygame.sprite.Sprite): # same class for a car
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab 8/race/Car.png")
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
    
    def spawn_n_move(self):
        screen.blit(self.image, self.rect) # draw a car
        pressed = pygame.key.get_pressed() # moving tracking
        if self.rect.left > 0 and pressed[pygame.K_LEFT]: self.rect.move_ip(-20, 0)
        if self.rect.right < size[0] and pressed[pygame.K_RIGHT]: self.rect.move_ip(20, 0)
        if self.rect.top > 0 and pressed[pygame.K_UP]: self.rect.move_ip(0, -20)
        if self.rect.bottom < size[1] and pressed[pygame.K_DOWN]: self.rect.move_ip(0, 20)

class Coin(pygame.sprite.Sprite): # class for coin
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab 8/race/Coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(25, size[0]-25), random.randint(25, size[1]-25))
        self.amount = 0
    def spawn_n_move(self): # method for creating a coin
        self.rect.center = (random.randint(25, size[0]-25), random.randint(25, size[1]-25))
    def collect(self, car: MainCar):
        if pygame.sprite.collide_rect(car, self): # cheking for collecting coin
            self.kill()
            self.spawn_n_move()
            self.amount += 1

player = MainCar()
enemy = Enemy()
coin = Coin()

all_enemies = pygame.sprite.Group() # create groups for entities
all_enemies.add(enemy)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

while not done:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5
        if event.type == pygame.QUIT:
            done = True
    
    screen.fill((255, 255, 255))
    for entuty in all_sprites:
        entuty.spawn_n_move()
    screen.blit(coin.image, coin.rect)
    coin.collect(player)

    if pygame.sprite.spritecollideany(player, all_enemies): # endgame screen will appear after collision of main car and enemies contact 
        for entity in all_sprites:
            entity.kill() # killing all entities
        screen.fill((255,255,255))
        screen.blit(go_font.render("GAME OVER", True, (255,0,0), (12,12,12)), (30,250))
        screen.blit(go_font.render(f"Score: {cars}", True, (0, 0, 0)), (120, 420))
        screen.blit(go_font.render(f"Coins: {coin.coins}", True, (0, 0, 0)), (120, 590))
        pygame.display.flip()
        sleep(2) # screen will displaying 2 sec
        done = True

    screen.blit(font.render(f"Cars: {cars}", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(f"Coins: {coin.amount}", True, (0, 0, 0)), (10, 30))
    pygame.display.flip()
    pygame.time.Clock().tick(60)