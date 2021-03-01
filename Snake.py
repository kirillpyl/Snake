import sqlite3
import pygame
import random

# Введение констант
FPS = 35
SPEED = 10
COUNT = -1


def start_screen():
    # Начальная заставка игры
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 35)
    text = font.render("HELLO! PRESS LEFT CLICK MOUSE!", True, (255, 100, 100))
    text_x = 480 // 2 - text.get_width() // 2
    text_y = 480 // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)
    pygame.display.flip()


def end_screen():
    # Конечная заставка игры
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("YOU LOSE!", True, (255, 100, 100))
    text_x = 480 // 2 - text.get_width() // 2
    text_y = 480 // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    # Вывод лучшего результата
    font2 = pygame.font.Font(None, 35)
    text2 = font2.render(f"Best score: {result[0]}", True, (0, 100, 160))
    screen.blit(text2, (320, 5))
    pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)
    square.draw_score()
    pygame.display.flip()


# Класс поля
class Square:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['-'] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # Метод отрисовки всего что есть на поле
    def render(self, screen):
        for i, value in enumerate(self.board):
            for j in range(len(value)):
                pygame.draw.rect(screen, (255, 255, 255),
                                 ((j * self.cell_size + self.left, i * self.cell_size + self.top),
                                  (self.cell_size, self.cell_size)), 1)
                # Отрисовка камней
                if value[j] == 'k':
                    screen.fill((101, 67, 33), ((j * self.cell_size + self.left, i * self.cell_size + self.top),
                                              (self.cell_size, self.cell_size)))
                # Отрисовка всего тела
                if value[j] == 'b':
                    screen.fill((0, 255, 0), ((j * self.cell_size + self.left, i * self.cell_size + self.top),
                                              (self.cell_size, self.cell_size)))
                # Отрисовка головы более темным цветом
                if value[j] == 'h':
                    screen.fill((130, 170, 100), ((j * self.cell_size + self.left, i * self.cell_size + self.top),
                                              (self.cell_size, self.cell_size)))
                    # Отрисовка глаз и носа
                    if change == 'RIGHT':
                        pygame.draw.circle(screen, (255, 255, 255), (j * self.cell_size + 8, i * self.cell_size + 8), 4)
                        pygame.draw.circle(screen, (255, 255, 255), (j * self.cell_size + 8, i * self.cell_size + 20), 4)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 8, i * self.cell_size + 8), 2)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 8, i * self.cell_size + 20), 2)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 20, i * self.cell_size + 15), 2)
                    elif change == 'DOWN':
                        pygame.draw.circle(screen, (255, 255, 255), (j * self.cell_size + 20, i * self.cell_size + 8), 4)
                        pygame.draw.circle(screen, (255, 255, 255), (j * self.cell_size + 8, i * self.cell_size + 8), 4)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 20, i * self.cell_size + 8), 2)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 8, i * self.cell_size + 8), 2)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 15, i * self.cell_size + 20), 2)
                    elif change == 'LEFT':
                        pygame.draw.circle(screen, (255, 255, 255), (j * self.cell_size + 20, i * self.cell_size + 20), 4)
                        pygame.draw.circle(screen, (255, 255, 255), (j * self.cell_size + 20, i * self.cell_size + 8), 4)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 20, i * self.cell_size + 20), 2)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 20, i * self.cell_size + 8), 2)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 10, i * self.cell_size + 15), 2)
                    elif change == 'UP':
                        pygame.draw.circle(screen, (255, 255, 255), (j * self.cell_size + 8, i * self.cell_size + 20), 4)
                        pygame.draw.circle(screen, (255, 255, 255), (j * self.cell_size + 20, i * self.cell_size + 20), 4)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 8, i * self.cell_size + 20), 2)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 20, i * self.cell_size + 20), 2)
                        pygame.draw.circle(screen, (0, 0, 0), (j * self.cell_size + 15, i * self.cell_size + 8), 2)

                # Отрисовка яблока
                if value[j] == 'a':
                    screen.fill((255, 0, 0), ((j * self.cell_size + self.left, i * self.cell_size + self.top),
                                              (self.cell_size, self.cell_size)))

    def draw_score(self):
        # Отрисовка счета в верхнем левом углу
        font = pygame.font.Font(None, 35)
        text = font.render(f"Score: {apples.ate} ", True, (0, 100, 160))
        screen.blit(text, (5, 5))
        pygame.display.flip()


# Класс змеи
class Snake:
    def __init__(self):
        # Координаты для головы змеи
        self.y_cord_head = 7
        self.x_cord_head = 7
        square.board[self.x_cord_head][self.y_cord_head] = 'h'
        square.board[7][6] = 'b'
        # Координаты для туловища змеи
        self.y_cord_head2 = 7
        self.x_cord_head2 = 6
        # Список с координатами всех частей змеи
        self.all_snake = [[self.y_cord_head2, self.x_cord_head2]]

    # Метод движения змеи
    def move_snake(self):
        global COUNT
        # Если змея не выезжает за пределы поля
        if 0 <= self.x_cord_head <= 15 and 0 <= self.y_cord_head <= 15:
            try:
                self.all_snake = [[self.y_cord_head, self.x_cord_head]] + self.all_snake
                square.board[self.y_cord_head][self.x_cord_head] = 'b'
                if change == 'RIGHT':
                    self.x_cord_head += 1
                elif change == 'LEFT':
                    self.x_cord_head -= 1
                elif change == 'UP':
                    self.y_cord_head -= 1
                elif change == 'DOWN':
                    self.y_cord_head += 1
                # Если змея врезается в себя, то игра заканчивается
                if [self.y_cord_head, self.x_cord_head] in self.all_snake:
                    COUNT = 1
                    return
                # Если змея врезается в камень, то игра заканчивается
                if square.board[self.y_cord_head][self.x_cord_head] == 'k':
                    COUNT = 1
                    return
                # Если змея съедает яблоко, она увеличивается
                if square.board[self.y_cord_head][self.x_cord_head] != 'a':
                    y, x = self.all_snake.pop()
                    square.board[y][x] = '-'
                square.board[self.y_cord_head][self.x_cord_head] = 'h'
            except:
                COUNT = 1
        # Если змея выезжает за пределы поля
        else:
            COUNT = 1

    def check_validate_direction(self, change, change_to):
        # Проверка на то, что бы не было выбрано противоположное направление движения
        if any((change == "RIGHT" and not change_to == "LEFT",
             change == "LEFT" and not change_to == "RIGHT",
                change == "UP" and not change_to == "DOWN",
                change == "DOWN" and not change_to == "UP")):
            return True


# Класс яблоков
class Apples:
    def __init__(self, width, height, count_apples):
        self.width = width
        self.height = height
        self.ate = count_apples
        # Создание случайных координат для яблок
        self.x1 = random.randrange(self.width)
        self.y1 = random.randrange(self.height)
        # Проверка на то, что если координаты яблока совпадают с частью змеи, то выбираются новые координаты
        while [self.y1, self.x1] in snake.all_snake or square.board[self.y1][self.x1] == 'k':
            self.x1 = random.randrange(self.width)
            self.y1 = random.randrange(self.height)
        square.board[self.y1][self.x1] = 'a'

    # Метод отвечающий за поедание пищи змеей
    def eat(self):
        if square.board[self.y1][self.x1] == 'h':
            self.ate += 1
            self.increase_speed()
            self.__init__(16, 16, self.ate)
            if self.ate % 7 == 0:
                level2.generate_stones()

    # Метод для увеличения скорости при поедании количества яблок кратному 5
    def increase_speed(self):
        global FPS
        if self.ate % 5 == 0:
            FPS += self.ate // 5
        if self.ate > 2:
            level2.__init__(16, 16)


# Класс для препядствий
class Level2:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    # Метод генерации положений препядствий
    def generate_stones(self):
        if apples.ate > 1:
            # Создание случайных координат для препядствия
            self.x2 = random.randrange(self.width)
            self.y2 = random.randrange(self.height)
            # Если координата камня совпадает и уже имеющимся яблоком или со змеей, то координаты рандомно меняются
            while [self.y2, self.x2] in snake.all_snake or square.board[self.y2][self.x2] == 'a':
                self.x2 = random.randrange(self.width)
                self.y2 = random.randrange(self.height)
            square.board[self.y2][self.x2] = 'k'


if __name__ == '__main__':
    square = Square(16, 16)
    snake = Snake()
    apples = Apples(16, 16, 0)
    level2 = Level2(16, 16)

    time = pygame.time.Clock()
    change = change_to = 'RIGHT'
    pygame.init()
    pygame.display.set_caption('Snake')
    size = width, height = 480, 480
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        if COUNT == -1:
            # Вывод начального экрана
            start_screen()
        if COUNT == 0:
            # Проверка на то, было съедено яблоко
            apples.eat()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and COUNT == 0:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                # Вызов функции-проверки на допустимость изменения направления
                if snake.check_validate_direction(change, change_to):
                    # Если направление допустимое, то меняем значение направления
                    change = change_to
            # Если нажали на мышку до начала игры и она началась
            if event.type == pygame.MOUSEBUTTONUP and COUNT == -1:
                COUNT = 0
            # Если игра закончилась и нужно начать ее заново
            if COUNT == 1 and event.type == pygame.MOUSEBUTTONUP:
                # Создание новых объектов
                square = Square(16, 16)
                snake = Snake()
                apples = Apples(16, 16, 0)
                level2 = Level2(16, 16)
                COUNT = -1
        if COUNT == 0:
            snake.move_snake()
            screen.fill((0, 0, 0))
            square.render(screen)
            time.tick(FPS // SPEED)
            pygame.display.flip()
            square.draw_score()

        # Если игра закончилась
        if COUNT == 1:
            # Подключение БД
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            # Поиск максимального результата среди имеющихся
            result = max(cur.execute("""SELECT best_score FROM scores""").fetchall())
            # Если игра была начата впервые на компьютере, то
            if not result:
                result = cur.execute(f"""INSERT INTO scores(best_score) VALUES({apples.ate})""")
            # Если был установлен новый рекорд, то старый меняется на него
            elif result[0] < apples.ate:
                result = cur.execute(f"""UPDATE scores
                                    SET best_score == {apples.ate}
                                    WHERE best_score == {result[0]}""")
            # Сохранение изменений в БД
            con.commit()
            # Вывод конечного состояния экрана
            end_screen()