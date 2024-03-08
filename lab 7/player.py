from player_class import *
def event_handler(): # проверка событий
    global done
    for event in pygame.event.get():
        # close windows = quit
        if event.type == pygame.QUIT:
            done = 1
        
        # keyboard tap control
        # space = play/stop, right = next, left = previous, l = loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = 1
            if event.key == pygame.K_SPACE:
                song_list.play_pause()
                song_list.play_first_song()
                play_button.show_alternative = not play_button.show_alternative
            if event.key == pygame.K_RIGHT:
                song_list.play_next_song()
            elif event.key == pygame.K_LEFT:
                song_list.play_prev_song()
            if event.key == pygame.K_l:
                song_list.loop = not song_list.loop
                print(f"Loop is {song_list.loop}")
            if event.key == pygame.K_s:
                song_list.shuffle_list()
        
        if event.type == END_SONG:
            song_list.play_next_song()
            print("the song ended!")
        
        # button tap control
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_button.rect.collidepoint(event.pos):
                song_list.play_pause()
                song_list.play_first_song()
                play_button.show_alternative = not play_button.show_alternative
            if next_button.rect.collidepoint(event.pos):
                song_list.play_next_song()
            if prev_button.rect.collidepoint(event.pos):
                song_list.play_prev_song()
            if loop_button.rect.collidepoint(event.pos):
                song_list.loop = not song_list.loop
                print(f"Loop is {song_list.loop}")
            if shuffle_button.rect.collidepoint(event.pos):
                song_list.shuffle_list()

player_window = Player(screen, (player_w, player_h), (0, 0)) # создание окна плеера
if True: # создание кнопок
    shuffle_button = Button(player_window.surface, (50,50), (25, player_h - 75), "Shuffle", 20, acent_color, pygame.K_s, turn_on=False)
    all_buttons.append(shuffle_button)
    prev_button = Button(player_window.surface, (50,50), (shuffle_button.pos[0] + shuffle_button.size[0] + space_between_buttons, player_h - 75), "Prev", 20, acent_color, pygame.K_LEFT)
    all_buttons.append(prev_button)
    play_button = Button(player_window.surface, (150,50), (prev_button.pos[0] + prev_button.size[0] + space_between_buttons, player_h - 75), "Play", 20, acent_color, pygame.K_SPACE, "Pause")
    all_buttons.append(play_button)
    next_button = Button(player_window.surface, (50,50), (play_button.pos[0] + play_button.size[0] + space_between_buttons, player_h - 75), "Next", 20, acent_color, pygame.K_RIGHT)
    all_buttons.append(next_button)
    loop_button = Button(player_window.surface, (50,50), (next_button.pos[0] + next_button.size[0] + space_between_buttons, player_h - 75), "Loop", 20, acent_color, pygame.K_l, turn_on=False)
    all_buttons.append(loop_button)
song_list = Songs(songs) # создание списка песен
progress_bar = ProgressBar(player_window.surface) # создание прогресс бара
pic = SongPicture(player_window.surface) # создание картинки песни
volume_bar = Button(player_window.surface, (150, 50), (player_w - 175, player_h - 75), "Volume", 20, acent_color, pygame.MOUSEWHEEL) # создание ползунка громкости

while not done:
    event_handler()
    
    player_window.draw() # отображение окна плеера
    for button in all_buttons: # отображение всех кнопок
        button.draw()
    song_list.volume_changing() # изменение громкости
    progress_bar.draw(song_list) # отображение прогресс бара
    pic.draw() # отображение картинки песни
    volume_bar.fill(song_list) # отображение ползунка громкости, да он через костыль написан как кнопка, но это не важно
    
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)