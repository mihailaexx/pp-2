import pygame

player_w, player_h = 1280, 720 # 16x9 size
if player_w / player_h != 16 / 9:
    raise ValueError("The aspect ratio is not 16:9")
screen = pygame.display.set_mode((player_w, player_h))
pygame.init()

# vars
tool_buttons = []
color_buttons = []
shapes = []
points = []
current_tool = None
color_black = (4,4,4)
color_red = (255,0,0)
color_orange = (255,165,0)
color_yellow = (255,255,0)
color_green = (0,255,0)
color_blue = (0,0,255)
color_purple = (128,0,128)
current_color = color_black

done = 0
FPS = 60

def while_pressed_mouse_pos_tracking(points: list = []):
    if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos() not in points:
        points.append((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]-70))
    elif not pygame.mouse.get_pressed()[0] and points:
        points_copy = points.copy()
        points.clear()
        return points_copy

def eraser(current_color: tuple, screen: pygame.surface):
    pnts = while_pressed_mouse_pos_tracking(points)
    if pnts != None and len(pnts) > 1:
        pygame.draw.lines(screen, (255,255,255), False, pnts, 40)
        pygame.display.update()

def brush(current_color: tuple, screen: pygame.surface):
    pnts = while_pressed_mouse_pos_tracking(points)
    if pnts != None and len(pnts) > 1:
        pygame.draw.lines(screen, current_color, False, pnts, 2)
        pygame.display.update()

def line(current_color: tuple, screen: pygame.surface):
    pnts = while_pressed_mouse_pos_tracking(points)
    if pnts != None and len(pnts) > 1:
        pygame.draw.line(screen, current_color, pnts[0], pnts[-1], 2)
        pygame.display.update()

def rectangle(current_color: tuple, screen: pygame.surface):
    pnts = while_pressed_mouse_pos_tracking(points)
    if pnts != None and len(pnts) > 1:
        pos_x = pnts[-1][0] if (pnts[0][0] > pnts[-1][0]) else pnts[0][0]
        pos_y = pnts[-1][1] if (pnts[0][1] > pnts[-1][1]) else pnts[0][1]
        pygame.draw.rect(screen, current_color, (pos_x, pos_y, abs(pnts[0][0] - pnts[-1][0]), abs(pnts[0][1] - pnts[-1][1])), 2)
        pygame.display.update()

def elipse(current_color: tuple, screen: pygame.surface):
    pnts = while_pressed_mouse_pos_tracking(points)
    if pnts != None and len(pnts) > 1:
        pos_x = pnts[-1][0] if (pnts[0][0] > pnts[-1][0]) else pnts[0][0]
        pos_y = pnts[-1][1] if (pnts[0][1] > pnts[-1][1]) else pnts[0][1]
        pygame.draw.ellipse(screen, current_color, (pos_x, pos_y, abs(pnts[0][0] - pnts[-1][0]), abs(pnts[0][1] - pnts[-1][1])), 2)
        pygame.display.update()

def right_triangle(current_color: tuple, screen: pygame.surface):
    pnts = while_pressed_mouse_pos_tracking(points)
    if pnts != None and len(pnts) > 1:
        pygame.draw.lines(screen, current_color, True, [pnts[0], (pnts[0][0], pnts[-1][1]), pnts[-1]], 2)

def equilateral_triangle(current_color: tuple, screen: pygame.surface):
    pnts = while_pressed_mouse_pos_tracking(points)
    if pnts != None and len(pnts) > 1:
        pygame.draw.lines(screen, current_color, True, [pnts[-1], (pnts[0][0], pnts[-1][1]), ((abs(pnts[0][0]+pnts[-1][0])/2, pnts[0][1]))], 2)

def rhombus(current_color: tuple, screen: pygame.surface):
    pnts = while_pressed_mouse_pos_tracking(points)
    if pnts != None and len(pnts) > 1:
        pygame.draw.lines(screen, current_color, True, [(abs(pnts[0][0]+pnts[-1][0])/2, pnts[0][1]),(pnts[0][0], abs(pnts[0][1]+pnts[-1][1])/2),(abs(pnts[0][0]+pnts[-1][0])/2, pnts[-1][1]), (pnts[-1][0], abs(pnts[0][1]+pnts[-1][1])/2)], 2)

# def dashed_rectangle(surface, color, rect, dash_length = 6):
#     x1, y1, width, height = rect
#     x2, y2 = x1 + width, y1 + height
    
#     # Верхняя и нижняя границы
#     for x in range(x1, x2, dash_length + dash_length):
#         pygame.draw.line(surface, color, (x, y1), (min(x + dash_length, x2), y1))
#         pygame.draw.line(surface, color, (x, y2), (min(x + dash_length, x2), y2))
    
#     # Левая и правая границы
#     for y in range(y1, y2, dash_length + dash_length):
#         pygame.draw.line(surface, color, (x1, y), (x1, min(y + dash_length, y2)))
#         pygame.draw.line(surface, color, (x2, y), (x2, min(y + dash_length, y2)))

class InstrumentBar():
    def __init__(self, screen, pos: tuple, size: tuple) -> None:
        self.screen = screen
        self.size = size
        self.pos = pos
        self.surface = pygame.Surface(self.size)
        self.surface.fill((255,255,255))
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
    def draw(self):
        pygame.draw.rect(self.surface, color_black, (0, 0, self.size[0], self.size[1]), 3)
        self.screen.blit(self.surface, (self.pos[0], self.pos[1]))

class Canva():
    def __init__(self, screen, pos: tuple, size: tuple) -> None:
        self.screen = screen
        self.size = size
        self.pos = pos
        self.surface = pygame.Surface(self.size)
        self.surface.fill((255,255,255))
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
    def draw(self):
        pygame.draw.rect(self.surface, color_black, (0, 0, self.size[0], self.size[1]), 3)
        self.screen.blit(self.surface, (self.pos[0], self.pos[1]))
    # def track(self):
    #     if self.rect.collidepoint(pygame.mouse.get_pos()):
    #         pygame.draw.circle(self.screen, color_black, pygame.mouse.get_pos(), 2)

class Button():
    def __init__(self, screen: pygame.Surface, pos, size, text, instrument=current_tool, font_size=20, font_color=color_black, turn_on = None) -> None:
        self.screen = screen
        self.pos = pos # определение позиции кнопки на поверхности
        self.size = size # определение размер кнопки
        self.surface = pygame.Surface(self.size) # создание поверхности самой кнопки
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1]) # создание прямоугольника на поверхности
        self.turn_on = turn_on # определение переключаемая ли кнопка
        self.font = pygame.font.Font(None, font_size) # определение шрифта
        self.text = self.font.render(text, True, font_color) # отображение текста
        self.text_rect = self.text.get_rect(center=(size[0]/2, size[1]/2)) # цетрирование текста в кнопке
        self.instrument = instrument
         
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
            if self.turn_on: pygame.draw.rect(*gray_border) 
            else: pygame.draw.rect(*white)
        
        self.surface.blit(self.text, self.text_rect) # отображение текста
        self.screen.blit(self.surface, (self.pos[0], self.pos[1]))

class ColorButton():
    def __init__(self, screen: pygame.Surface, color, pos, size, turn_on = False) -> None:
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size
        self.surface = pygame.Surface(self.size)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.turn_on = turn_on
    def draw(self):
        
        def adjust_color(color, adjustment): # функция для изменения цвета
            return tuple(max(0, min(255, c + adjustment)) for c in color)
        
        black = (self.surface, (0, 0, 0), (0, 0, self.size[0], self.size[1]))
        dark_color = (self.surface, adjust_color(self.color, -20), (1, 1, self.size[0]-2, self.size[1]-2))
        deep_color_border = (self.surface, adjust_color(self.color, -55), (2, 2, self.size[0]-2, self.size[1]-2))
        color = (self.surface, self.color, (1, 1, self.size[0]-2, self.size[1]-2))
        
        pygame.draw.rect(*black)
        if self.rect.collidepoint(pygame.mouse.get_pos()): # чек если курсор на кнопке
            if pygame.mouse.get_pressed()[0]: # зажата LBM
                pygame.draw.rect(*deep_color_border)
            else: # просто навел
                if self.turn_on: pygame.draw.rect(*deep_color_border)
                else: pygame.draw.rect(*dark_color)
        else:
            if self.turn_on: pygame.draw.rect(*deep_color_border)
            else: pygame.draw.rect(*color)
        
        self.screen.blit(self.surface, (self.pos[0], self.pos[1]))

bar = InstrumentBar(screen, (0,0), (player_w,70))
canva = Canva(screen, (0,70), (player_w, player_h-70))

if True:
    clear_all_button = Button(bar.surface, (10,10), (50,50), "Clear")
    eraser_button = Button(bar.surface, (70,10), (50,50), "Eraser", eraser, turn_on=False)
    tool_buttons.append(eraser_button)
    brush_button = Button(bar.surface, (130,10), (50,50), "Brush", brush, turn_on=False)
    tool_buttons.append(brush_button)
    line_button = Button(bar.surface, (190,10), (50,50), "Line", line, turn_on=False)
    tool_buttons.append(line_button)
    circle_button = Button(bar.surface, (250,10), (50,50), "Circle", elipse, turn_on=False)
    tool_buttons.append(circle_button)
    rectangle_button = Button(bar.surface, (310,10), (50,50), "Rect", rectangle, turn_on=False)
    tool_buttons.append(rectangle_button)
    square_button = Button(bar.surface, (370,10), (50,50), "Square", None, turn_on=False)
    tool_buttons.append(square_button)
    right_triangle_button = Button(bar.surface, (430,10), (50,50), "R. T.", right_triangle, turn_on=False)
    tool_buttons.append(right_triangle_button)
    equilateral_triangle_button = Button(bar.surface, (490,10), (50,50), "E. T.", equilateral_triangle, turn_on=False)
    tool_buttons.append(equilateral_triangle_button)
    rhombus_button = Button(bar.surface, (550,10), (50,50), "Rhomb", rhombus, turn_on=False)
    tool_buttons.append(rhombus_button)
    color_red_button = ColorButton(bar.surface, color_red, (610,10), (50,50))
    color_buttons.append(color_red_button)
    color_orange_button = ColorButton(bar.surface, color_orange, (670,10), (50,50))
    color_buttons.append(color_orange_button)
    color_yellow_button = ColorButton(bar.surface, color_yellow, (730,10), (50,50))
    color_buttons.append(color_yellow_button)
    color_green_button = ColorButton(bar.surface, color_green, (790,10), (50,50))
    color_buttons.append(color_green_button)
    color_blue_button = ColorButton(bar.surface, color_blue, (850,10), (50,50))
    color_buttons.append(color_blue_button)
    color_purple_button = ColorButton(bar.surface, color_purple, (910,10), (50,50))
    color_buttons.append(color_purple_button)
    color_black_button = ColorButton(bar.surface, color_black, (970,10), (50,50))
    color_buttons.append(color_black_button)

def event_handler():
    global done, current_tool, current_color
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in tool_buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()) and button.turn_on != None:
                    for butttton in tool_buttons:
                        butttton.turn_on = False
                    button.turn_on = True
                    current_tool = button.instrument
            for color_button in color_buttons:
                if color_button.rect.collidepoint(pygame.mouse.get_pos()):
                    for button in color_buttons:
                        button.turn_on = False
                    color_button.turn_on = True
                    current_color = color_button.color
    if clear_all_button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        canva.surface.fill((255,255,255))
        pygame.display.update()

while not done:
    event_handler()
    clear_all_button.draw()
    for button in tool_buttons:
        button.draw()
    for color_button in color_buttons:
        color_button.draw()
    bar.draw()
    canva.draw()
    # canva.track()
    
    if current_tool and canva.rect.collidepoint(pygame.mouse.get_pos()):
        current_tool(current_color, canva.surface)
    
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)