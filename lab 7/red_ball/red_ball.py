import pygame

pygame.init()
size = (900, 900)
screen = pygame.display.set_mode(size)
done = False
is_blue = True
x = 25
y = 25
radius = 50

ball_color = (255,0,0)

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y -= 20
    if pressed[pygame.K_DOWN]: y += 20
    if pressed[pygame.K_LEFT]: x -= 20
    if pressed[pygame.K_RIGHT]: x += 20
    x = max(radius, min(x, size[0]-radius))
    y = max(radius, min(y, size[1]-radius))

    pygame.draw.circle(screen, ball_color, (x,y), radius)
    pygame.display.flip()
    clock.tick(60)