import pygame, random, time
pygame.init()
size = (1000, 900)
screen = pygame.display.set_mode(size)
screen_net = pygame.Surface(size, pygame.SRCALPHA)
for i in range(1,20):
    pygame.draw.line(screen_net, (0,0,0,130), (0, i*50), (1000, i*50))
    pygame.draw.line(screen_net, (0,0,0,130), (i*50, 0), (i*50, 900))

def crete_entity(): # create tuple of coords
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
level = 0
font = pygame.font.Font(None, 24)
go_font = pygame.font.Font(None, 128)

last_move = None
FPS = 2
done = False
game_over = False

log = open("snake_log.txt", "w") # decide to add a log -\_(>.<)_/-
log.write('''---START GAME---
''')

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
    screen.blit(screen_net, (0,0))
    # apple
    pygame.draw.circle(screen, apple_color, apple_pos, snake_part_radius)
    if (x,y) == apple_pos:
        apple_pos = crete_entity()
        # Check if apple position overlaps with snake parts
        while apple_pos in snake_parts:
            apple_pos = crete_entity()
        log.write(f'''YOU COLLECT APPLE
New apple apear in {apple_pos}

''')
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
    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))
    
    # moving depended on last pressed key
    if last_move == pygame.K_UP: y-=snake_part_diametr
    elif last_move == pygame.K_DOWN: y+=snake_part_diametr
    elif last_move == pygame.K_LEFT: x-=snake_part_diametr
    elif last_move == pygame.K_RIGHT: x+=snake_part_diametr
    
    # collision
    if (x, y) in snake_parts and len(snake_parts) != 1:
        game_over = True
        log.write(f'''YOU LOSE
Reason: crash into yourself
Score:{score}''')
    
    # borders
    if check_boundary():
        game_over = True
        log.write(f'''YOU LOSE
Reason: out of border
Score:{score}
''')
    
    # maybe someone wanna check this test???? :)
    if len(snake_parts) == 20*18:
        done = True
        log.write("YOU WIN!!!")
    level = score//2
    
    if game_over: # add a game over screen
        game_over_text = go_font.render("GAME OVER", True, (255,0,0), (12,12,12))
        screen.blit(game_over_text, (250,300))
        pygame.display.flip()
        time.sleep(2)  # Add a 5-second delay
        done = True
    
    pygame.display.flip()
    pygame.time.Clock().tick(0.25*level+2)
log.write("---END GAME---")
log.close()