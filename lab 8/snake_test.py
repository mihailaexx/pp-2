import pygame, random

pygame.init()
size = (1000, 900)
screen = pygame.display.set_mode(size)

def crete_entity():
    return (random.randint(1,18)*50+25, random.randint(1,16)*50+25)
def check_boundary():
    if x < snake_part_radius or x > size[0] - snake_part_radius or y < snake_part_radius or y > size[1] - snake_part_radius:
        return True
    return False

# snake consist of balls
x = crete_entity()[0] # head x cord
y = crete_entity()[1] # head y cord
snake_part_radius = 25
snake_part_diametr = 2 * snake_part_radius
snake_color = (0,100,0)
snake_parts = [(x,y)] # add head manually

apple_color = (230,0,0)
apple_pos = crete_entity()

# score
score = 0
font = pygame.font.Font(None, 36)

last_move = None
FPS = 2
done = False


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
        apple_pos = crete_entity()
        # Check if apple position overlaps with snake parts
        while apple_pos in snake_parts:
            apple_pos = crete_entity()
        print(f'''YOU COLLECT APPLE
New apple apear in {apple_pos}''')
        snake_parts.append((x,y))
        score += 1
    
    # pos updating
    for i in range(len(snake_parts) - 1, 0, -1):
        snake_parts[i] = snake_parts[i - 1]
    if snake_parts:
        snake_parts[0] = (x,y)
    
    # drawing snake
    for part in snake_parts:
        pygame.draw.circle(screen, snake_color, part, snake_part_radius)
    
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    # moving depended on last pressed key
    if last_move == pygame.K_UP: y-=snake_part_diametr
    elif last_move == pygame.K_DOWN: y+=snake_part_diametr
    elif last_move == pygame.K_LEFT: x-=snake_part_diametr
    elif last_move == pygame.K_RIGHT: x+=snake_part_diametr
    
    # collision
    if (x, y) in snake_parts and len(snake_parts) != 1:
        done = True
        print(f'''YOU LOSE
Reason: crash into yourself
Score:{score}''')
    
    # borders
    if check_boundary():
        done = True
        print(f'''YOU LOSE
Reason: out of border
Score:{score}''')
    
    # maybe someone wanna check this test???? :)
    if len(snake_parts) == 20*18:
        done = True
        print("YOU WIN!!!")

    pygame.display.flip()
    pygame.time.Clock().tick(2+(score/8))