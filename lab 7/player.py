import pygame
import random

screen = pygame.display.set_mode((640, 400))
pygame.mixer.init()

# Constants
END_SONG = pygame.USEREVENT + 1
VOLUME_CHANGE = 5
FPS = 30

# Variables
volume = 10
play = False
done = False

# Initialize pygame mixer and clock
pygame.mixer.music.set_endevent(END_SONG)
clock = pygame.time.Clock()

# List of songs
_songs = ["Unlock2e_LS2_4.1.mp3","Unlock2e_LS2_4.2.mp3","Unlock2e_LS2_4.3.mp3","Unlock2e_LS2_4.4.mp3"]
_currently_playing_song = None

def play_a_different_song():
    global _currently_playing_song, _songs
    next_song = random.choice(_songs)
    while next_song == _currently_playing_song:
        next_song = random.choice(_songs)
    _currently_playing_song = next_song
    pygame.mixer.music.load(next_song)
    pygame.mixer.music.play()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
            play = not play
        if event.type == END_SONG:
            play_a_different_song()
            print("Song end")

    # pygame.mixer.music.load(_songs[0])

    screen.fill((255,255,255))
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: volume = min(100, volume + VOLUME_CHANGE)
    if pressed[pygame.K_DOWN]: volume = max(0, volume - VOLUME_CHANGE)
    pygame.mixer.music.set_volume(volume / 100)
    
    if pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]: 
        play_a_different_song()
        print("Song skipped")
    
    if play: 
        if pygame.mixer.music.get_busy() == 0:
            play_a_different_song()
            print("Song played")
    else: 
        pygame.mixer.music.stop()
        print("Song stopped")
    
    pygame.display.flip()
    clock.tick(FPS)