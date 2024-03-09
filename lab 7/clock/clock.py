# broo there's no hands.png or smth like this, only full image
# so i'll use my own clock image and hands
import pygame, datetime

pygame.init()
screen = pygame.display.set_mode((900, 900)) # 900 x 900 window

clock_image = pygame.image.load("clock.png")

clock_min = pygame.image.load("line_m2.png")
clock_min_rect = clock_min.get_rect(center=(450, 450))
clock_sec = pygame.image.load("line_s2.png")
clock_sec_rect = clock_sec.get_rect(center=(450, 450))

clock = pygame.time.Clock()

done = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = 1
    screen.fill((255,255,255))
    screen.blit(clock_image, (150,150))
    
    now = datetime.datetime.now()
    angle_sec = now.second * (-6)
    angle_min = now.minute * (-6) + now.second * (-0.1)
    
    rotated_clock_sec = pygame.transform.rotate(clock_sec, angle_sec) # rotating
    rotated_clock_min = pygame.transform.rotate(clock_min, angle_min)
    
    rotated_rect_sec = rotated_clock_sec.get_rect(center=clock_sec_rect.center) # centering
    rotated_rect_min = rotated_clock_min.get_rect(center=clock_min_rect.center)
    
    screen.blit(rotated_clock_sec, rotated_rect_sec.topleft) # placing
    screen.blit(rotated_clock_min, rotated_rect_min.topleft)
    
    pygame.display.flip()
    clock.tick(1)