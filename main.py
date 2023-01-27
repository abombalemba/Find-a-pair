import pygame
from random import randint
from time import sleep

from json import load, dump
from subprocess import Popen


pygame.init()
X, Y = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((X, Y))

clock = pygame.time.Clock()
running_menu = running_game = running_settings = running_stats = running_choose = running_choose_online = running_end = True
FPS = 60

COLOR_OPENED_BOX = (50, 210, 200)
COLOR_CLOSED_BOX = (130, 255, 210)
COLOR_TEXT = (20, 15, 10)
COLOR_EXIT = (255, 35, 0)
COLOR_SETTINGS = (80, 90, 85)
COLOR_STATS = (150, 250, 150)
COLOR_BACKGROUND = (170, 150, 220)
COLOR_PLAYER1 = (180, 20, 0)
COLOR_PLAYER2 = (100, 150, 240)
COLOR_PLAYER3 = (50, 200, 50)
COLOR_PLAYER4 = (255, 220, 50)
COLOR_PLAYERS = []

L = 100
FIELDS = {}

BOXES = []
OPENED_BOXES = []
DELETED_BOXES = []
PLAYERS = {}
COUNT_PLAYERS = 0
PLAYERS_POS = ((X * 0.15, Y * 0.7), (X * 0.8, Y * 0.7), (X * 0.15, Y * 0.2), (X * 0.8, Y * 0.2))
CIRCLES_POS = ((0, Y), (X, Y), (0, 0), (X, 0))
I = 1

double = False
user = 'пользователь'

x, y = X * 0.275, Y * 0.1
for i in range(L // 10):
    for j in range(L // 10):
        BOXES.append((pygame.Rect(x, y, 50, 50), int(str(i) + str(j))))
        x += 75
    y += 75
    x = X * 0.275

button_start = pygame.Rect(X * 0.35, Y * 0.3, X * 0.3, Y * 0.2)
button_stats = pygame.Rect(X * 0.15, Y * 0.6, X * 0.3, Y * 0.2)
button_settings = pygame.Rect(X * 0.55, Y * 0.6, X * 0.3, Y * 0.2)

button_online = pygame.Rect(X * 0.15, Y * 0.3, X * 0.3, Y * 0.2)
button_2_players = pygame.Rect(X * 0.55, Y * 0.3, X * 0.3, Y * 0.2)
button_3_players = pygame.Rect(X * 0.15, Y * 0.6, X * 0.3, Y * 0.2)
button_4_players = pygame.Rect(X * 0.55, Y * 0.6, X * 0.3, Y * 0.2)

button_exit = pygame.Rect(X * 0.9, 0, X * 0.1, Y * 0.05)
text_exit = pygame.font.SysFont('Comic Sans MS', 32).render('выход', True, (255, 255, 255))
text_title = pygame.font.SysFont('Comic Sans MS', 100, bold=False).render('НАЙДИ ПАРУ', True, COLOR_TEXT)

font50 = pygame.font.SysFont('Comic Sans MS', 50)
font60 = pygame.font.SysFont('Comic Sans MS', 60)
font70 = pygame.font.SysFont('Comic Sans MS', 70)

BALLS = []
COLOR_BALLS = ((140, 120, 190), (130, 110, 180), (120, 100, 170))


class Ball:
    def __init__(self, x, y, radius) -> None:
        self.x, self.y, self.radius = x, y, radius
        if self.radius < 20: self.color = COLOR_BALLS[0]
        elif self.radius < 40: self.color = COLOR_BALLS[1]
        elif self.radius <= 50: self.color = COLOR_BALLS[2]


def main() -> None:
    global running_menu, COLOR_PLAYERS

    while running_menu:
        screen.fill(COLOR_BACKGROUND)
        balls()

        pygame.draw.rect(screen, COLOR_PLAYER2, button_start)
        pygame.draw.rect(screen, COLOR_PLAYER3, button_stats)
        pygame.draw.rect(screen, COLOR_PLAYER4, button_settings)

        screen.blit(font60.render('играть', True, COLOR_TEXT), (X * 0.43, Y * 0.35))
        screen.blit(font60.render('настройки', True, COLOR_TEXT), (X * 0.6, Y * 0.65))
        screen.blit(font60.render('статистика', True, COLOR_TEXT), (X * 0.2, Y * 0.65))

        pygame.draw.rect(screen, COLOR_EXIT, button_exit)
        screen.blit(text_exit, (X * 0.92, Y * 0.005))
        screen.blit(text_title, (X * 0.3, Y * 0.1))
        screen.blit(pygame.font.SysFont('Verdana', 30).render(f'{int(clock.get_fps())}', True, (0, 0, 0)), (10, Y * 0.95))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_exit.collidepoint(event.pos):
                    running_menu = False
                elif button_start.collidepoint(event.pos):
                    choose()
                elif button_stats.collidepoint(event.pos):
                    statistic()
                elif button_settings.collidepoint(event.pos):
                    settings()

            if event.type == pygame.KEYDOWN:
                pass

        pygame.display.update()
        clock.tick(FPS)


def choose() -> None:
    global running_choose, COUNT_PLAYERS, COLOR_PLAYERS

    while running_choose:
        screen.fill(COLOR_BACKGROUND)
        balls()

        pygame.draw.rect(screen, COLOR_PLAYER1, button_online)
        pygame.draw.rect(screen, COLOR_PLAYER2, button_2_players)
        pygame.draw.rect(screen, COLOR_PLAYER3, button_3_players)
        pygame.draw.rect(screen, COLOR_PLAYER4, button_4_players)

        screen.blit(font70.render('выберите режим'.upper(), True, COLOR_TEXT), (X * 0.3, Y * 0.1))
        screen.blit(font50.render('онлайн', True, COLOR_TEXT), (X * 0.23, Y * 0.35))
        screen.blit(font50.render('2 игрока', True, COLOR_TEXT), (X * 0.63, Y * 0.35))
        screen.blit(font50.render('3 игрока', True, COLOR_TEXT), (X * 0.23, Y * 0.65))
        screen.blit(font50.render('4 игрока', True, COLOR_TEXT), (X * 0.63, Y * 0.65))

        screen.blit(pygame.font.SysFont('Verdana', 30).render(f'{int(clock.get_fps())}', True, (0, 0, 0)), (10, Y * 0.95))

        pygame.draw.rect(screen, (255, 36, 0), button_exit)
        screen.blit(text_exit, (X * 0.92, Y * 0.005))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_choose = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_exit.collidepoint(event.pos):
                    running_choose = False
                    main()
                elif button_online.collidepoint(event.pos):
                    choose_online()
                elif button_2_players.collidepoint(event.pos):
                    COLOR_PLAYERS = [COLOR_PLAYER1, COLOR_PLAYER2]
                    COUNT_PLAYERS = 2
                    game()
                elif button_3_players.collidepoint(event.pos):
                    COLOR_PLAYERS = [COLOR_PLAYER1, COLOR_PLAYER2, COLOR_PLAYER3]
                    COUNT_PLAYERS = 3
                    game()
                elif button_4_players.collidepoint(event.pos):
                    COLOR_PLAYERS = [COLOR_PLAYER1, COLOR_PLAYER2, COLOR_PLAYER3, COLOR_PLAYER4]
                    COUNT_PLAYERS = 4
                    game()

            if event.type == pygame.KEYDOWN:
                pass

        pygame.display.update()
        clock.tick(FPS)
    running_choose = True


def choose_online() -> None:
    global running_choose_online

    button_create_room = pygame.Rect(X * 0.15, Y * 0.3, X * 0.3, Y * 0.2)
    button_join_room = pygame.Rect(X * 0.55, Y * 0.3, X * 0.3, Y * 0.2)

    while running_choose_online:
        screen.fill(COLOR_BACKGROUND)
        balls()

        pygame.draw.rect(screen, COLOR_PLAYER3, button_create_room)
        pygame.draw.rect(screen, COLOR_PLAYER4, button_join_room)

        screen.blit(font50.render('создать комнату', True, COLOR_TEXT), (X * 0.17, Y * 0.35))
        screen.blit(font50.render('войти в комнату', True, COLOR_TEXT), (X * 0.57, Y * 0.35))
        screen.blit(pygame.font.SysFont('Verdana', 30).render(f'{int(clock.get_fps())}', True, (0, 0, 0)), (10, Y * 0.95))

        pygame.draw.rect(screen, (255, 36, 0), button_exit)
        screen.blit(text_exit, (X * 0.92, Y * 0.005))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_choose_online = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_exit.collidepoint(event.pos):
                    running_choose_online = False
                elif button_create_room.collidepoint(event.pos):
                    print('go create')
                    Popen(['python3', 'server.py'])
                elif button_join_room.collidepoint(event.pos):
                    print('go join')
                    Popen(['python3', 'client.py'])

            if event.type == pygame.KEYDOWN:
                pass

        pygame.display.update()
        clock.tick(FPS)
    running_choose_online = True


def game() -> None:
    global running_game, COUNT_PLAYERS, double, I

    make_fields()
    for i in range(COUNT_PLAYERS):
        PLAYERS[f'{i}'] = [0, PLAYERS_POS[i]]

    lets_sleep, running_game = False, True
    while running_game:
        if lets_sleep:
            lets_sleep = False
            sleep(1)
            OPENED_BOXES.clear()

        screen.fill(COLOR_BACKGROUND)

        if len(DELETED_BOXES) == len(BOXES):
            running_game = False
            end(COLOR_PLAYERS[I % COUNT_PLAYERS])

        for i in range(L // 10):
            for j in range(L // 10):
                if BOXES[int(str(i) + str(j))][1] in DELETED_BOXES:
                    continue
                if BOXES[int(str(i) + str(j))] is True:
                    pygame.draw.rect(screen, COLOR_OPENED_BOX, BOXES[int(str(i) + str(j))][0])
                else:
                    pygame.draw.rect(screen, COLOR_CLOSED_BOX, BOXES[int(str(i) + str(j))][0])

        pygame.draw.circle(screen, COLOR_PLAYERS[(I + 1) % COUNT_PLAYERS], CIRCLES_POS[(I + 1) % COUNT_PLAYERS], Y * 0.3)
        screen.blit(pygame.font.SysFont('Verdana', 30).render(f'{int(clock.get_fps())}', True, (0, 0, 0)), (10, Y * 0.95))

        pygame.draw.rect(screen, (255, 36, 0), button_exit)
        screen.blit(text_exit, (X * 0.92, Y * 0.005))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_exit.collidepoint(event.pos):
                    running_game = False
                    choose()

                for box in BOXES:
                    if box[0].collidepoint(event.pos):
                        if box[1] in DELETED_BOXES:
                            continue
                        OPENED_BOXES.append(box)
                        if double: double = False; I += 1
                        else: double = True

                        if len(OPENED_BOXES) == 2:
                            if FIELDS[f'{OPENED_BOXES[0][1]}'] == FIELDS[f'{OPENED_BOXES[1][1]}']:
                                PLAYERS[f'{I % COUNT_PLAYERS}'][0] += 1
                                DELETED_BOXES.append(OPENED_BOXES[0][1]), DELETED_BOXES.append(OPENED_BOXES[1][1])
                                I -= 1
                            lets_sleep = True

        for box in OPENED_BOXES:
            pygame.draw.rect(screen, COLOR_OPENED_BOX, box[0])
            screen.blit(pygame.font.SysFont('Verdana', 40).render(f'{FIELDS[f"{box[1]}"]}', True, COLOR_TEXT), (box[0].x + 10, box[0].y))

        for player in range(len(PLAYERS)):
            screen.blit(pygame.font.SysFont('Verdana', 100).render(f'{PLAYERS[f"{player}"][0]}', True, COLOR_TEXT), PLAYERS[f"{player}"][1])

        pygame.display.update()
        clock.tick(FPS)
    running_game = True


def settings() -> None:
    global running_settings

    while running_settings:
        screen.fill(COLOR_BACKGROUND)
        balls()

        pygame.draw.rect(screen, COLOR_EXIT, button_exit)
        screen.blit(text_exit, (X * 0.92, Y * 0.005))

        screen.blit(pygame.font.SysFont('Verdana', 30).render(f'{int(clock.get_fps())}', True, (0, 0, 0)), (10, Y * 0.95))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_settings = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_exit.collidepoint(event.pos):
                    running_settings = False

            if event.type == pygame.KEYDOWN:
                pass

        pygame.display.update()
        clock.tick(FPS)
    running_settings = True


def statistic() -> None:
    global running_stats

    while running_stats:
        screen.fill(COLOR_BACKGROUND)
        balls()

        pygame.draw.rect(screen, COLOR_EXIT, button_exit)
        screen.blit(text_exit, (X * 0.92, Y * 0.005))

        screen.blit(pygame.font.SysFont('Verdana', 30).render(f'{int(clock.get_fps())}', True, (0, 0, 0)), (10, Y * 0.95))

        screen.blit(font70.render('статистика:'.upper(), True, (20, 15, 11)), (X * 0.1, Y * 0.05))
        screen.blit(font70.render('достижения:'.upper(), True, (20, 15, 11)), (X * 0.55, Y * 0.05))

        y_ = Y * 0.2
        for i in DATA[user]['статистика']:
            screen.blit(font50.render(f'{i} - {DATA[user]["статистика"][i]}', True, (20, 15, 11)), (X * 0.15, y_))
            y_ += Y * 0.1

        y_ = Y * 0.2
        for i in DATA[user]['достижения']:
            screen.blit(font50.render(f'{i} - {DATA[user]["достижения"]}', True, (20, 15, 11)), (X * 0.6, y_))
            y_ += Y * 0.1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_stats = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_exit.collidepoint(event.pos):
                    running_stats = False

            if event.type == pygame.KEYDOWN:
                pass

        pygame.display.update()
        clock.tick(FPS)
    running_stats = True


def end(winner: tuple) -> None:
    global running_end

    if winner == COLOR_PLAYER1: winner = 'синий'
    elif winner == COLOR_PLAYER2: winner = 'красный'
    elif winner == COLOR_PLAYER3: winner = 'зеленый'
    elif winner == COLOR_PLAYER4: winner = 'желтый'

    while running_end:
        screen.fill(COLOR_BACKGROUND)
        balls()

        screen.blit(pygame.font.SysFont('Comic Sans MS', 50).render(f'Выиграл: {winner}!', True, COLOR_TEXT), (X * 0.4, Y * 0.4))
        pygame.draw.rect(screen, COLOR_EXIT, button_exit)
        screen.blit(text_exit, (X * 0.92, Y * 0.005))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_end = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_exit.collidepoint(event.pos):
                    running_end = False
                    main()

            if event.type == pygame.KEYDOWN:
                pass

        pygame.display.update()
        clock.tick(FPS)
    running_end = True


def make_fields() -> None:
    global FIELDS, DELETED_BOXES, OPENED_BOXES

    for i in range(L // 2):
        rnd = randint(0, 9)
        FIELDS[str(L // 2 + i)] = rnd
        FIELDS[str(i)] = rnd
    OPENED_BOXES.clear(), DELETED_BOXES.clear()


def balls() -> None:
    if randint(1, 50) == 1:
        BALLS.append(Ball(randint(0, X), randint(-Y, 0), randint(1, 50)))

    for ball in BALLS:
        if ball.radius < 20: ball.y += 3
        elif ball.radius < 40: ball.y += 2
        else: ball.y += 1
        pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.radius)


def load_data() -> dict:
    new_data = {user: {}}
    with open('data.json', 'r', encoding='utf-8') as file:
        sp = load(file)
        try:
            for i in sp[user]:
                new_data[user][i] = {}
                for j in sp[user][i]:
                    #print(sp[user][i][j])
                    #print(new_data)
                    new_data[user][i][j] = sp[user][i][j]
        except KeyError:
            pass
        print(new_data, type(new_data))
        for i in new_data[user]:
            print(i)
            for j in new_data[user][i]:
                print(new_data[user][i][j])
        file.close()
    return new_data


def save_data() -> None:
    pass


def load_sounds() -> None:
    if DATA[user]['настройки']['музыка'] == 'on':
        music = pygame.mixer.Sound('sounds/music.mp3')
        music.play(-1)
    if DATA[user]['настройки']['звуки'] == 'on':
        sound = pygame.mixer.Sound('sounds/click.mp3')
        sound.play(-1)


if __name__ == '__main__':
    DATA = load_data()
    load_sounds()
    main()
