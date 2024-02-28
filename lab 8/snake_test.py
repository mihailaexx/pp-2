import pygame, random

pygame.init()
size = (1000, 900)
screen = pygame.display.set_mode(size)

# snake consist of balls
x = 25 # head x cord
y = 25 # head y cord
snake_part_radius = 25
snake_part_diametr = 2 * snake_part_radius
snake_color = (0,128,0)
snake_parts = [(x,y)] # add head manually

apple_color = (230,0,0)
apple_pos = (random.randint(1,18)*50+25, random.randint(1,16)*50+25)

last_move = None
FPS = 2
done = False




clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        # quit cheking
        if event.type == pygame.QUIT:
            done = True
        # key cheking
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: 
            if event.key == pygame.K_UP and last_move != pygame.K_DOWN:
                last_move = pygame.K_UP
            elif event.key == pygame.K_DOWN and last_move != pygame.K_UP:
                last_move = pygame.K_DOWN
            elif event.key == pygame.K_LEFT and last_move != pygame.K_RIGHT:
                last_move = pygame.K_LEFT
            elif event.key == pygame.K_RIGHT and last_move != pygame.K_LEFT:
                last_move = pygame.K_RIGHT
    screen.fill((255, 255, 255))
    
    # apple
    pygame.draw.circle(screen, apple_color, apple_pos, snake_part_radius)
    if (x,y) == apple_pos:
        print("YOU COLLECT APPLE")
        apple_pos = (random.randint(1,18)*50+25, random.randint(1,16)*50+25)
        # Check if apple position overlaps with snake parts
        while apple_pos in snake_parts:
            apple_pos = (random.randint(1,18)*50+25, random.randint(1,16)*50+25)
        print(apple_pos)
        snake_parts.append((x,y))
    
    # pos updating
    for i in range(len(snake_parts) - 1, 0, -1):
        snake_parts[i] = snake_parts[i - 1]
    if snake_parts:
        snake_parts[0] = (x,y)
    
    # drawing snake
    for part in snake_parts:
        pygame.draw.circle(screen, snake_color, part, snake_part_radius)
    
    # moving depended on last pressed key
    if last_move == pygame.K_UP: y-=snake_part_diametr
    elif last_move == pygame.K_DOWN: y+=snake_part_diametr
    elif last_move == pygame.K_LEFT: x-=snake_part_diametr
    elif last_move == pygame.K_RIGHT: x+=snake_part_diametr
    
    # collision
    if (x, y) in snake_parts and len(snake_parts) != 1:
        done = True
        print("YOU LOSE")
    
    # borders
    if x >= snake_part_radius and x <= size[0]-snake_part_radius: x = max(snake_part_radius, min(x, size[0]-snake_part_radius))
    else: 
        done = True
        print("YOU LOSE")
    if y >= snake_part_radius and y <= size[1]-snake_part_radius: y = max(snake_part_radius, min(y, size[1]-snake_part_radius))
    else: 
        done = True
        print("YOU LOSE")
    
    pygame.display.flip()
    clock.tick(FPS)