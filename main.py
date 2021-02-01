# Библиотеки

import pygame
import random

# Список цветов от фигур
colors_1 = [
    '#ff0000',
    '#f8173e',
    '#ba021e',
    '#f75216',
    '#ff5349',
    '#f23f1f',
]
colors_3 = [
    '#0000ff',
    '#00001a',
    '#a366ff',
    '#5d76cb',
    '#7fc7ff',
    '#00ffff',
]

colors_2 = [
    '#ffff00',
    '#ccff00',
    '#f3da0b',
    '#ccad00',
    '#ffa161',
    '#ffe14d',
]

colors_4 = [
    '#008000',
    '#00ff00',
    '#7cfc00',
    '#bfff00',
    '#0bda51',
    '#00fa9a',
]

colors_5 = [
    '#808080',
    '#898176',
    '#a18594',
    '#979aaa',
    '#9c9c9c',
    '#99958c',
]

colors_used = colors_1


# Создание класса

class Figure:
    x = 0
    y = 0

    # Все позиции фигур, и их возможные перевертыши :D
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.colors_used = random.randint(1, len(colors_used) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


# Создание класса тетриса

class Tetris:
    # переменные класса тетрис
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    # Высота, длина и т.д рамки.
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        icon = pygame.image.load('Иконка.png')
        pygame.display.set_icon(icon)
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    # Функция создания фигуры
    def new_figure(self):
        self.figure = Figure(3, 0)

    def cross(self):

        crossing = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        crossing = True
        return crossing

    # Функция рисования сеточки
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    # Функция падения фигуры
    def go_space(self):
        while not self.cross():
            self.figure.y += 1
        self.figure.y -= 1
        self.stop()

    # Функция спуска фигуры
    def go_down(self):
        self.figure.y += 1
        if self.cross():
            self.figure.y -= 1
            self.stop()

    # Цикл остановки фигуры
    def stop(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.colors_used
        self.break_lines()
        self.new_figure()
        if self.cross():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.cross():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.cross():
            self.figure.rotation = old_rotation


# Инициализация pygame
pygame.init()

# Определите несколько цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Размер рамки
size = (400, 500)
screen = pygame.display.set_mode(size)

# Название программы
pygame.display.set_caption("Тетрис")

# Цикл,пока пользователь не нажмет кнопку закрытия.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False

# Во время игры...
while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    # Присвоение к кнопкам действия
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)
            if event.key == pygame.K_1:
                colors_used = colors_1
            if event.key == pygame.K_2:
                colors_used = colors_2
            if event.key == pygame.K_3:
                colors_used = colors_3
            if event.key == pygame.K_4:
                colors_used = colors_4
            if event.key == pygame.K_5:
                colors_used = colors_5

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False

    # Цвет фона
    screen.fill(WHITE)

    # Положение фигур

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, BLACK, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors_used[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors_used[game.figure.colors_used],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)

    # Создание своего оттенка финального цвета в зависимости от темы.
    color_1 = '#ff0000'
    if colors_used == colors_1:
        color_1 = '#ff496c'
    if colors_used == colors_2:
        color_1 = '#ffd700'
    if colors_used == colors_3:
        color_1 = '#660099'
    if colors_used == colors_4:
        color_1 = '#5da130'
    if colors_used == colors_5:
        color_1 = BLACK

    # Финальный текст
    text = font.render("Cчёт: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Вы проиграли.", True, color_1)
    text_game_over1 = font1.render("Нажми ESC", True, color_1)

    # Вывод текста и его расположение.
    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [2, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

# Закрытие окна
pygame.quit()
