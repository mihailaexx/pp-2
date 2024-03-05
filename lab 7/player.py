import pygame

screen_w, screen_h = 640, 400
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

# Constants
END_SONG = pygame.USEREVENT + 1
VOLUME_CHANGE = 0.5
FPS = 30

# Variables
volume = 1
volume1 = volume
play = 0
loop = 0
done = 0
song_length = 0

font = pygame.font.Font(None, 24)
# creating button surfaces
button_play_surface = pygame.Surface((150, 50))
button_next_surface = pygame.Surface((50, 50))
button_prev_surface = pygame.Surface((50, 50))
button_loop_surface = pygame.Surface((50, 50))
button_volume_surface = pygame.Surface((100, 50))
progress_bar_surface = pygame.Surface((540, 4))
# create var's with diff texts
play_text = font.render("Play", True, (54, 50, 135))
pause_text = font.render("Pause", True, (54, 50, 135))
next_text = font.render("Next", True, (54, 50, 135))
prev_text = font.render("Prev", True, (54, 50, 135))
loop_text = font.render("Loop", True, (54, 50, 135))
time_now_text = font.render("0:00", True, (54, 50, 135))
time_duration_text = font.render("0:00", True, (54, 50, 135))
track_name = font.render("None", True, (54, 50, 135))
button_volume_text = font.render(f"{volume}", True, (0,0,0))
# centering text in button
play_text_rect = play_text.get_rect(center=(button_play_surface.get_width()/2, button_play_surface.get_height()/2))
pause_text_rect = pause_text.get_rect(center=(button_play_surface.get_width()/2, button_play_surface.get_height()/2))
next_text_rect = next_text.get_rect(center=(button_next_surface.get_width()/2, button_next_surface.get_height()/2))
prev_text_rect = prev_text.get_rect(center=(button_prev_surface.get_width()/2, button_prev_surface.get_height()/2))
loop_text_rect = loop_text.get_rect(center=(button_loop_surface.get_width()/2, button_loop_surface.get_height()/2))
button_volume_text_rect = button_volume_text.get_rect(center=(button_volume_surface.get_width()/2, button_volume_surface.get_height()/2))
# create black rectangles for layout
button_play_rect = pygame.Rect((screen_w-150)/2, screen_h-90, 150, 50)
button_next_rect = pygame.Rect((screen_w-150)/2+165, screen_h-90, 50, 50)
button_prev_rect = pygame.Rect((screen_w-150)/2-65, screen_h-90, 50, 50)
button_loop_rect = pygame.Rect(((screen_w-150)/2+230, screen_h-90, 50, 50))
progress_bar_rect = pygame.Rect(50, 276, screen_w-50, 4)
button_volume_rect = pygame.Rect((screen_w-150)/2-180, screen_h-90, 100, 50)
# Initialize pygame mixer and clock
pygame.mixer.music.set_endevent(END_SONG)
clock = pygame.time.Clock()

# List of songs
songs = ["Unlock2e_LS2_4.1.mp3","Unlock2e_LS2_4.2.mp3","Unlock2e_LS2_4.3.mp3","Unlock2e_LS2_4.4.mp3"] # used a english audios for example
currently_playing_song = -1


def play_next_song(): # через костыли ну да ;)
    global currently_playing_song, songs, loop, song_length, track_name
    if loop:
        if currently_playing_song == -1:
            currently_playing_song = 0
    elif currently_playing_song == -1:
            currently_playing_song = 0
    else:
        currently_playing_song = (currently_playing_song + 1) % len(songs)
    print(f"played next song №{currently_playing_song+1}")
    track_name = font.render(f"{songs[currently_playing_song]}", True, (54, 50, 135))
    song_length = 0
    pygame.mixer.music.load(f"lab 7/{songs[currently_playing_song]}")
    pygame.mixer.music.play()

def play_previous_song():
    global currently_playing_song, songs, loop, song_length, track_name
    if loop:
        pass
    elif currently_playing_song == -1:
        currently_playing_song = 0
    else:
        currently_playing_song = (currently_playing_song - 1) % len(songs)
    print(f"played previous song №{currently_playing_song+1}")
    track_name = font.render(f"{songs[currently_playing_song]}", True, (54, 50, 135))
    song_length = 0
    pygame.mixer.music.load(f"lab 7/{songs[currently_playing_song]}")
    pygame.mixer.music.play()

def looop():
    global loop
    loop = not loop
    print("Loop on") if loop else print("Loop off")

def fill_progress(): # filling progress bar depending on second of track
    global currently_playing_song, song_length, time_now_text, time_duration_text
    if play:
        pos_now = pygame.mixer.music.get_pos()
        time_now_text = font.render(f"{pos_now//1000//60}:{pos_now//1000%60}", True, (54, 50, 135))
        if not song_length:
            song_length = pygame.mixer.Sound(f"lab 7/{songs[currently_playing_song]}").get_length()
            time_duration_text = font.render(f"{round(song_length)//60}:{round(song_length)%60}", True, (54, 50, 135))
        colored_part = 540/song_length * (pos_now / 1000)
        pygame.draw.rect(progress_bar_surface, (255,255,255), (0, 0, progress_bar_rect[2], 2))
        pygame.draw.rect(progress_bar_surface, (54, 50, 135), (0, 0, colored_part, 2))
    screen.blit(time_now_text, (50,285))
    screen.blit(time_duration_text, (559,285))

def fill_volume():
    global volume, button_volume_surface, button_volume_text, button_volume_text_rect, button_volume_rect
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: 
        volume = min(100, volume + VOLUME_CHANGE)
        button_volume_text = font.render(f"{volume}", True, (0,0,0))
        button_volume_text_rect = button_volume_text.get_rect(center=(button_volume_surface.get_width()/2, button_volume_surface.get_height()/2))
    if pressed[pygame.K_DOWN]: 
        volume = max(0, volume - VOLUME_CHANGE)
        button_volume_text = font.render(f"{volume}", True, (0,0,0))
        button_volume_text_rect = button_volume_text.get_rect(center=(button_volume_surface.get_width()/2, button_volume_surface.get_height()/2))
    pygame.mixer.music.set_volume(volume / 100)
    pygame.draw.rect(button_volume_surface, (54, 50, 135), (2, 2, volume-4, 46))

while not done:
    for event in pygame.event.get():
        # close windows = quit
        if event.type == pygame.QUIT:
            done = 1
        # space = play/stop
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
            play = not play
        # right = next, left = previous, l = loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                play_next_song()
            elif event.key == pygame.K_LEFT:
                play_previous_song()
            if event.key == pygame.K_l:
                looop()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # button click = play/stop
            if button_play_rect.collidepoint(event.pos):
                if play:
                    play = 0
                    print("Button \"Pause\" clicked!")
                else:
                    play = 1
                    print("Button \"Play\" clicked!")
            # button play next even if paused
            if button_next_rect.collidepoint(event.pos):
                if currently_playing_song != -1: 
                    play_next_song()
                    play = 1
                    pygame.draw.rect(progress_bar_surface, (0,0,0), (0,0,540,2))
                    print("Button \"Next\" clicked!")
            # button previous next even if paused
            if button_prev_rect.collidepoint(event.pos):
                if currently_playing_song != -1: 
                    play_previous_song()
                    play = 1
                    pygame.draw.rect(progress_bar_surface, (0,0,0), (0,0,540,2))
                    print("Button \"Prev\" clicked!")
            # button loop switcher
            if button_loop_rect.collidepoint(event.pos):
                looop()
                print("Button \"Loop\" clicked!")
            # set vol to 0 and backup if clicked
            if button_volume_rect.collidepoint(event.pos):
                if volume > 0:
                    volume1 = volume
                    volume = 0
                    button_volume_text = font.render(f"{volume}", True, (0, 0, 0))
                else:
                    volume = volume1
                    button_volume_text = font.render(f"{volume}", True, (0, 0, 0))
                button_volume_text_rect = button_volume_text.get_rect(center=(button_volume_surface.get_width()/2, button_volume_surface.get_height()/2))
    # volume changer

    # play button behaviour
    if play: 
        if pygame.mixer.music.get_busy() == 0:
            if currently_playing_song == -1:
                play_next_song()
                print("Start playing")
            else:
                pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

    screen.fill((255,255,255))
    fill_progress()
    fill_volume()
    
    if not play: button_play_surface.blit(play_text, play_text_rect)
    else: button_play_surface.blit(pause_text, pause_text_rect)
    button_next_surface.blit(next_text, next_text_rect)
    button_prev_surface.blit(prev_text, prev_text_rect)
    button_loop_surface.blit(loop_text, loop_text_rect)
    button_volume_surface.blit(button_volume_text, button_volume_text_rect)
    screen.blit(button_play_surface, (button_play_rect[0], button_play_rect[1]))
    screen.blit(button_next_surface, (button_next_rect[0], button_next_rect[1]))
    screen.blit(button_prev_surface, (button_prev_rect[0], button_prev_rect[1]))
    screen.blit(button_loop_surface, (button_loop_rect[0],button_loop_rect[1]))
    screen.blit(progress_bar_surface, (progress_bar_rect[0], progress_bar_rect[1]))
    screen.blit(button_volume_surface, (button_volume_rect[0], button_volume_rect[1]))
    screen.blit(track_name, (50,255))
    
    
    # button play
    if button_play_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_play_surface, (230,230,230), (2, 2, 146, 46))
    else:
        pygame.draw.rect(button_play_surface, (0, 0, 0), (0, 0, 150, 50))
        pygame.draw.rect(button_play_surface, (255, 255, 255), (2, 2, 146, 46))
    
    # button next
    if button_next_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_next_surface, (230,230,230), (2, 2, 46, 46))
    else:
        pygame.draw.rect(button_next_surface, (0, 0, 0), (0, 0, 50, 50))
        pygame.draw.rect(button_next_surface, (255, 255, 255), (2, 2, 46, 46))
    
    # button prev
    if button_prev_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_prev_surface, (230,230,230), (2, 2, 46, 46))
    else:    
        pygame.draw.rect(button_prev_surface, (0, 0, 0), (0, 0, 50, 50))
        pygame.draw.rect(button_prev_surface, (255, 255, 255), (2, 2, 46, 46))
    
    # button loop 
    if button_loop_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_loop_surface, (230,230,230), (2, 2, 46, 46))
    else:
        pygame.draw.rect(button_loop_surface, (0, 0, 0), (0, 0, 50, 50))
        pygame.draw.rect(button_loop_surface, (255, 255, 255), (2, 2, 46, 46))
    
    # volume loop
    if button_volume_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_volume_surface, (230,230,230), (2, 2, 96, 46))
    else:
        pygame.draw.rect(button_volume_surface, (0, 0, 0), (0, 0, 100, 50))
        pygame.draw.rect(button_volume_surface, (255, 255, 255), (2, 2, 96, 46))
    
    pygame.display.flip()
    clock.tick(FPS)