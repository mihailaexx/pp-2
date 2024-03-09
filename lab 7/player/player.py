import pygame
from random import shuffle # для шафла рееально функцию придумали, она изменяет сам список, поэтому регай новый при нажатии кнопки

player_w, player_h = 640, 360 # 16x9 size
screen = pygame.display.set_mode((player_w, player_h))
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

# const
END_SONG = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(END_SONG)
VOLUME_CHANGE = 1
FPS = 60

# vars
space_between_buttons = 15
acent_color = (54, 50, 135)
all_buttons = []
songs = ["Unlock2e_LS2_4.1.mp3","Unlock2e_LS2_4.2.mp3","Unlock2e_LS2_4.3.mp3","Unlock2e_LS2_4.4.mp3"]

done = 0

class Player():
    def __init__(self, screen: pygame.Surface, size: tuple, pos: tuple) -> None:
        self.screen = screen # выбор поверхности где будет распологаться плеер
        self.size = size # определение размер плеера
        if size[0] / size[1] != 16 / 9:
            raise ValueError("Player size must have a 16x9 ratio")
        self.pos = pos # определение позиции плеера на поверхности
        if pos[0] < 0 or pos[1] < 0:
            raise ValueError("Player position must be positive")
        if pos[0] + size[0] > screen.get_width() or pos[1] + size[1] > screen.get_height():
            raise ValueError("Player size must fit in the screen")
        self.surface = pygame.Surface(self.size)
        pygame.display.set_caption("Player: pending")
    def draw(self): # отображение окна
        self.screen.blit(self.surface, (self.pos[0], self.pos[1]))
        self.surface.fill(acent_color) # добавил рамку по приколу
        self.surface.fill((255, 255, 255), (10, 10, self.size[0]-20, self.size[1]-20))

class Songs():
    def __init__(self, list: list, isplaying: bool = 0, number: int = None, name: str = None, volume: int = 1, loop = False, shuffle = False) -> None:
        self.list = list
        self.list_backup = None
        self.isplaying = isplaying
        self.number = number
        self.name = name
        self.volume = volume
        self.loop = loop
        self.shuffle = shuffle
        self.song_length = 0
    def load_song(self):
        self.number %= len(self.list)
        self.name = self.list[self.number]
        pygame.mixer.music.load(f"lab 7/player/{self.name}")
        self.song_length = pygame.mixer.Sound(f"lab 7/player/{self.name}").get_length()
        pygame.mixer.music.play()
        pygame.display.set_caption(f"Player: playing - {self.name}")
        self.isplaying = 1
    def play_first_song(self):
        if self.number == None:
            self.number = 0
            self.load_song()
            print("Player launched first time")
    def play_next_song(self):
        if self.number != None: # не дает нажать кнопку если не выполнен первый запуск
            if self.loop: pass
            else: self.number += 1
            self.load_song()
            print(f"Play next song({self.number+1})")
    def play_prev_song(self):
        if self.number != None: # не дает нажать кнопку если не выполнен первый запуск
            if self.loop: pass
            else: self.number -= 1
            self.load_song()
            print(f"Play previous song({self.number+1})")
    def play_pause(self):
        if self.isplaying:
            pygame.mixer.music.pause()
            pygame.display.set_caption(f"Player: paused - {self.name}")
            print("Paused")
        else:
            pygame.mixer.music.unpause()
            pygame.display.set_caption(f"Player: playing - {self.name}")
            print("Unpaused")
        self.isplaying = not self.isplaying
    def volume_changing(self):
        pygame.mixer.music.set_volume(self.volume / 100)
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.volume = min(100, self.volume + VOLUME_CHANGE)
        elif pressed[pygame.K_DOWN]: 
            self.volume = max(0, self.volume - VOLUME_CHANGE)
    def shuffle_list(self): # здесь gpt и copilot помог, каюсь
        if not self.shuffle:
            if self.number == None:
                self.list_backup = self.list[:]
                shuffle(self.list)
            else:
                if self.list_backup == None:
                    self.list_backup = self.list[:]
                tail = self.list[self.number+1:]
                shuffle(tail)
                self.list[self.number+1:] = tail
            print("Shuffled, list is:")
            print(*self.list)
            self.shuffle = not self.shuffle
        else:
            self.list = self.list_backup[:]
            print("Unshuffled, list is:")
            print(*self.list)
            self.shuffle = not self.shuffle

class Button():
    def __init__(self, screen: pygame.Surface, size: tuple, pos: tuple, text: str, font_size: int, font_color: tuple, key: pygame.key = None, alternative_text = None, turn_on = None) -> None:
        self.screen = screen # выбор поверхности где будут распологаться кнопки
        self.size = size # определение размер кнопки
        self.surface = pygame.Surface(self.size) # создание поверхности самой кнопки
        self.font = pygame.font.Font(None, font_size) # определение шрифта
        self.font_color = font_color # определение цвета шрифта
        self.text = self.font.render(text, True, font_color) # отображение текста
        self.text_rect = self.text.get_rect(center=(size[0]/2, size[1]/2)) # цетрирование текста в кнопке
        self.pos = pos # определение чпозиции кнопки на поверхности
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1]) # создание прямоугольника на поверхности 
        if alternative_text != None: # если есть альтернативный текст
            self.alternative_text = self.font.render(alternative_text, True, font_color) # отображение альтернативного текста
            self.alternative_text_rect = self.alternative_text.get_rect(center=(size[0]/2, size[1]/2)) # центрирование альтернативного текста
        self.show_alternative = 0 # показывать ли альтернативный текст
        self.turn_on = turn_on
        self.key = key
    def draw(self):
        black = (self.surface, (0, 0, 0), (0, 0, self.size[0], self.size[1])) # черный
        lightgray = (self.surface, (235, 235, 235), (1, 1, self.size[0]-2, self.size[1]-2)) # светло-серый
        gray_border = (self.surface, (200, 200, 200), (2, 2, self.size[0]-2, self.size[1]-2)) # серый и большие края
        white = (self.surface, (255, 255, 255), (1, 1, self.size[0]-2, self.size[1]-2)) # белый
        # поведение кнопки
        pygame.draw.rect(*black) 
        if self.rect.collidepoint(pygame.mouse.get_pos()): # чек если курсор на кнопке
            if pygame.mouse.get_pressed()[0]: # зажата LBM
                pygame.draw.rect(*gray_border)
            else: # просто навел
                if self.turn_on: pygame.draw.rect(*gray_border)
                else: pygame.draw.rect(*lightgray)
        else:
            if pygame.key.get_pressed()[self.key]: # зажата клавиша на клавиатуре
                pygame.draw.rect(*gray_border)
            else:
                if self.turn_on: pygame.draw.rect(*gray_border) 
                else: pygame.draw.rect(*white)
        if self.show_alternative: self.surface.blit(self.alternative_text, self.alternative_text_rect) # отображение альтернативного текста
        else: self.surface.blit(self.text, self.text_rect) # отображение текста
        self.screen.blit(self.surface, (self.pos[0], self.pos[1])) # отображение кнопки на поверхности
    def fill(self, song: Songs):
        self.text = self.font.render(str(song.volume), True, (0,0,0))
        self.text_rect = self.text.get_rect(center=(self.size[0]/2, self.size[1]/2))
        pygame.draw.rect(self.surface, (255,255,255), (1, 1, self.size[0]-2, self.size[1]-2))
        pygame.draw.rect(self.surface, acent_color, (1, 1, 1.48*song.volume, self.size[1]-2))
        self.surface.blit(self.text, self.text_rect)
        self.screen.blit(self.surface, (self.pos[0], self.pos[1]))

class ProgressBar():
    # упустим некоторые значения при объявлении тк прогресс бар один на весь плеер
    def __init__(self, screen: pygame.Surface, font_size: int = 24, font_color: tuple = acent_color, size: tuple = (player_w-50, 5), pos: tuple = (25, player_h - 95), color: tuple = acent_color) -> None:
        self.screen = screen
        self.size = size
        self.surface = pygame.Surface(self.size)
        self.font = pygame.font.Font(None, font_size)
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.font_color = font_color
    def draw(self, songs: Songs):
        pos_now = pygame.mixer.music.get_pos()
        if songs.isplaying:
            # полоса прогресса
            colored_part = self.size[0]/songs.song_length*(pos_now/1000)
            pygame.draw.rect(self.surface, (255,255,255), (0, 0, self.rect[2], 3))
            pygame.draw.rect(self.surface, (54, 50, 135), (0, 0, colored_part, 3))
        self.screen.blit(self.surface, (self.pos[0], self.pos[1]))
        
        # текущее время
        mins, secs = divmod(pos_now // 1000, 60)
        current_time_text = self.font.render(f"{mins}:{secs:02d}", True, self.font_color)
        current_time_rect = current_time_text.get_rect(topleft=(25, player_h - 115))
        screen.blit(current_time_text, current_time_rect)
        # общая длинна
        total_mins, total_secs = divmod(round(songs.song_length), 60)
        total_time = f"{total_mins}:{total_secs:02d}"  # Добавление ведущего нуля для секунд
        total_time_text = self.font.render(total_time, True, self.font_color)
        total_time_rect = total_time_text.get_rect(topright=(player_w - 25, player_h - 115))
        screen.blit(total_time_text, total_time_rect)
        # название песни
        song_name_text = self.font.render(songs.name, True, self.font_color)
        song_name_rect = song_name_text.get_rect(center=(player_w/2, player_h - 108))
        screen.blit(song_name_text, song_name_rect)

class SongList():
    pass # та ну его xD

class SongPicture():
    def __init__(self, screen: pygame.Surface, size: tuple = (205, 205), pos: tuple = (25,25)) -> None:
        self.screen = screen
        self.size = size
        self.pos = pos
        self.surface = pygame.Surface(size)
        self.image = pygame.image.load("lab 7/pic.png") # поидее тут надо загружать изображение песни
        self.image_rect = self.image.get_rect(center=(size[0]/2, size[1]/2))
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
    def draw(self):
        self.surface.blit(self.image, self.image_rect)
        self.screen.blit(self.surface, (self.pos[0], self.pos[1]))

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
volume_bar = Button(player_window.surface, (150, 50), (player_w - 175, player_h - 75), "Volume", 20, acent_color) # создание ползунка громкости

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
                loop_button.turn_on = not loop_button.turn_on 
                print(f"Loop is {song_list.loop}")
            if event.key == pygame.K_s:
                shuffle_button.turn_on = not shuffle_button.turn_on 
                song_list.shuffle_list()
        
        # song end control
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
                loop_button.turn_on = not loop_button.turn_on 
                print(f"Loop is {song_list.loop}")
            if shuffle_button.rect.collidepoint(event.pos):
                shuffle_button.turn_on = not shuffle_button.turn_on 
                song_list.shuffle_list()

while not done: # основной цикл
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