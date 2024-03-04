import pygame
import random

screen = pygame.display.set_mode((640, 400))
pygame.init()
pygame.mixer.init()

# Constants
END_SONG = pygame.USEREVENT + 1
VOLUME_CHANGE = 0.25
FPS = 30

# Variables
volume = 1
play = False
loop = False
done = False

font = pygame.font.Font(None, 24)
# creating button surfaces
button_play_surface = pygame.Surface((150, 50))
button_next_surface = pygame.Surface((50, 50))
button_prev_surface = pygame.Surface((50, 50))
progress_bar_surface = pygame.Surface((540, 2))
# create var's with diff texts
play_text = font.render("Play", True, (0, 0, 0))
pause_text = font.render("Pause", True, (0, 0, 0))
next_text = font.render("Next", True, (0, 0, 0))
prev_text = font.render("Prev", True, (0, 0, 0))
# centering text in button
play_text_rect = play_text.get_rect(center=(button_play_surface.get_width()/2, button_play_surface.get_height()/2))
pause_text_rect = play_text.get_rect(center=(button_play_surface.get_width()/2, button_play_surface.get_height()/2))
next_text_rect = next_text.get_rect(center=(button_next_surface.get_width()/2, button_next_surface.get_height()/2))
prev_text_rect = prev_text.get_rect(center=(button_next_surface.get_width()/2, button_next_surface.get_height()/2))
# create black rectangles for layout
button_rect = pygame.Rect(245, 310, 150, 50)
button2_rect = pygame.Rect(410, 310, 50, 50)
button3_rect = pygame.Rect(180, 310, 50, 50)
progress_bar_rect = pygame.Rect(50, 280, 540, 2)

# Initialize pygame mixer and clock
pygame.mixer.music.set_endevent(END_SONG)
clock = pygame.time.Clock()

# List of songs
songs = ["Unlock2e_LS2_4.1.mp3","Unlock2e_LS2_4.2.mp3","Unlock2e_LS2_4.3.mp3","Unlock2e_LS2_4.4.mp3"] # used a english audios for example
currently_playing_song = -1


def play_next_song(): # через костыли ну да ;)
    global currently_playing_song, songs, loop
    next_song = currently_playing_song + 1
    if loop:
        currently_playing_song += 1
    elif next_song < len(songs):
        currently_playing_song = next_song
    else:
        currently_playing_song = 0
    print(f"played next song №{currently_playing_song+1}")
    pygame.mixer.music.load(f"lab 7/{songs[currently_playing_song]}")
    pygame.mixer.music.play()

def play_previous_song():
    global currently_playing_song, songs, loop
    previous_song = currently_playing_song -1
    if loop:
        currently_playing_song += 1
    elif previous_song >= 0:
        currently_playing_song = previous_song
    else:
        currently_playing_song = len(songs)-1
    print(f"played previous song №{currently_playing_song+1}")
    pygame.mixer.music.load(f"lab 7/{songs[currently_playing_song]}")
    pygame.mixer.music.play()

def fill_progress():
    global currently_playing_song
    if currently_playing_song != -1: 
        track_len = pygame.mixer.Sound(f"lab 7/{songs[currently_playing_song]}").get_length()
    pos_now = pygame.mixer.music.get_pos()
    if pos_now != -1: 
        pygame.time.delay(1000)
        colored_part = 540/track_len * (pos_now / 1000)
        pygame.draw.rect(progress_bar_surface, (255,0,0), (0, 0, colored_part, 2))
    
    
while not done:
    for event in pygame.event.get():
        
        # close windows = quit
        if event.type == pygame.QUIT:
            done = True
            
        # space = play/stop
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
            play = not play
        
        # right = next, left = previous
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                play_next_song()
            elif event.key == pygame.K_LEFT:
                play_previous_song()
                print("Previous song")
        
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # button click = play/stop
            if button_rect.collidepoint(event.pos):
                print("Button \"Play\" clicked!")
                if play:
                    play = False
                else:
                    play = True
            # button play next even if paused
            if button2_rect.collidepoint(event.pos):
                if currently_playing_song != -1: 
                    play_next_song()
                    play = True
                    pygame.draw.rect(progress_bar_surface, (0,0,0), (0,0,540,2))
                    print("Button \"Next\" clicked!")
            # button previous next even if paused
            if button3_rect.collidepoint(event.pos):
                if currently_playing_song != -1: 
                    play_previous_song()
                    play = True
                    pygame.draw.rect(progress_bar_surface, (0,0,0), (0,0,540,2))
                    print("Button \"Prev\" clicked!")



    screen.fill((255,255,255))
    fill_progress()
    
    if not play: button_play_surface.blit(play_text, play_text_rect)
    else: button_play_surface.blit(pause_text, pause_text_rect)
    button_next_surface.blit(next_text, next_text_rect)
    button_prev_surface.blit(prev_text, prev_text_rect)
    screen.blit(button_play_surface, (button_rect[0], button_rect[1]))
    screen.blit(button_next_surface, (button2_rect[0], button2_rect[1]))
    screen.blit(button_prev_surface, (button3_rect[0], button3_rect[1]))
    screen.blit(progress_bar_surface, (progress_bar_rect[0], progress_bar_rect[1]))
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: volume = min(100, volume + VOLUME_CHANGE)
    if pressed[pygame.K_DOWN]: volume = max(0, volume - VOLUME_CHANGE)
    pygame.mixer.music.set_volume(volume / 100)
    
    
    # button play
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_play_surface, (230,230,230), (1, 1, 148, 48))
    else:
        pygame.draw.rect(button_play_surface, (0, 0, 0), (0, 0, 150, 50))
        pygame.draw.rect(button_play_surface, (255, 255, 255), (1, 1, 148, 48))
    
    # button next
    if button2_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_next_surface, (230,230,230), (1, 1, 48, 48))
    else:
        pygame.draw.rect(button_next_surface, (0, 0, 0), (0, 0, 50, 50))
        pygame.draw.rect(button_next_surface, (255, 255, 255), (1, 1, 48, 48))
    
    # button prev
    if button3_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_prev_surface, (230,230,230), (1, 1, 48, 48))
    else:    
        pygame.draw.rect(button_prev_surface, (0, 0, 0), (0, 0, 50, 50))
        pygame.draw.rect(button_prev_surface, (255, 255, 255), (1, 1, 48, 48))
    
    if play: 
        if pygame.mixer.music.get_busy() == 0:
            if currently_playing_song == -1:
                play_next_song()
                print("Start playing")
            else:
                pygame.mixer.music.unpause()
                print("Song unpaused")
    else:
        pygame.mixer.music.pause()
        print("Song paused")
    
    pygame.display.flip()
    clock.tick(FPS)