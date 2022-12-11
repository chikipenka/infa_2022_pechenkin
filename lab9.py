import time

import pygame
from pygame.draw import *
from random import randint
from math import *

pygame.init()

number_of_balls = 1  # количество мишеней
FPS = 100

width = 1200
height = 800
screen = pygame.display.set_mode((width, height))


class Balls:  # класс мишеней
    def __init__(self):
        self.x = randint(100, width - 100)
        self.y = randint(100, height - 100)
        self.r = randint(40, 80)
        self.color = [randint(0, 255), randint(0, 255), randint(0, 255)]
        self.x_speed = randint(-500, 500) / 100
        self.y_speed = randint(-500, 500) / 100
        circle(screen, self.color, (self.x, self.y), self.r)

    def __update__(self):  # движение мишени
        self.x += self.x_speed
        self.y += self.y_speed
        self.y_speed += randint(-20, 20) / 100
        self.x_speed += randint(-20, 20) / 100
        circle(screen, self.color, (self.x, self.y), self.r)

    def __reflection__(self):  # отражение мишени от стен
        if self.x >= width - self.r or self.x <= self.r:
            self.x_speed *= -1
        if self.y >= height - self.r or self.y <= self.r:
            self.y_speed *= -1


class bullet:  # класс снарядов
    def __init__(self, x, y, current_time, start_time, length):
        self.start_time = start_time
        self.angle = atan(x / y)
        if current_time > 5:
            self.life = 5
        else:
            self.life = current_time
        self.x = 100 * cos(self.angle)
        self.y = height - 100 * sin(self.angle)
        self.r = 25
        self.color = [randint(0, 255), randint(0, 255), randint(0, 255)]
        self.x_speed = 3 + self.life ** 2 * sin(self.angle) * 3  # скорость снаряда от времени
        self.y_speed = 3 + self.life ** 2 * cos(self.angle) * 3
        circle(screen, self.color, (self.x, self.y), self.r)

    def __update__(self, time):  # движение снаряда
        self.x += self.x_speed
        if not (abs(self.y - height) < self.r - 3 and abs(self.y_speed) <= 3):
            self.y_speed -= 0.3
            if self.y > height - self.r:
                self.y = height - self.r - 1
            else:
                self.y -= self.y_speed
        circle(screen, self.color, (self.x, self.y), self.r)

    def __reflection__(self):  # отражение снаряда от стена
        if self.x >= width - self.r or self.x <= self.r:
            self.x_speed *= -1
        if self.y >= height - self.r or self.y <= self.r:
            self.y_speed *= -1


class gun:  # класс пушки
    def __init__(self, x, y, length=100):
        y = height - y
        if y <= 0:  # убираем возможное деление на ноль
            y = 1
        if x <= 0:
            x = 1
        self.length = length
        self.angle = atan(x / y)  # угол наклона курсора
        self.x1 = 50
        self.y1 = height
        self.x2 = 50 + self.length * sin(self.angle)
        self.y2 = height - self.length * cos(self.angle)
        self.x3 = self.x2 - 50 * cos(self.angle)
        self.y3 = self.y2 - 50 * sin(self.angle)
        self.x4 = self.x1 - 50 * cos(self.angle)
        self.y4 = height - 50 * sin(self.angle)
        self.color = [255, 0, 255]
        self.base_x = 0
        self.base_y = height - 50 * sin(self.angle) + self.x4 * tan(self.angle) ** -1
        self.base_color = [0, 255, 255]

        polygon(screen, self.color, [[self.x1, self.y1], [self.x2, self.y2], [self.x3, self.y3], [self.x4, self.y4]])
        polygon(screen, self.base_color,
                [[0, height], [self.base_x, self.base_y], [self.x4, self.y4], [self.x1, self.y1]])


clock = pygame.time.Clock()
game_balls = [Balls() for i in range(number_of_balls)]  # создание списка мишеней
finished = False
x = 0
y = 0
new_length = 100
real_gun = gun(x, y)
real_bullet = list()  # список пуль
click = False  # проверка на то, что нажатие закончилось
time1 = 0
time2 = 0
previous_click = False  # проверка на то, что предыдущее нажатие закончилось
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEMOTION:
            x = event.pos[0]
            y = event.pos[1]
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
            time1 = time.time()
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
            time2 = time.time()
    if click:  # рисуем пушку
        if time.time() - time1 > 5:
            real_gun.__init__(x, y, 200)
        else:
            real_gun.__init__(x, y, 100 + 100 * (time.time() - time1) / 5)
    else:
        real_gun.__init__(x, y)
    if previous_click and not click:  # косание закончилось
        real_bullet.append(bullet(x, y, time2 - time1, time1, 100 + 100 * (time.time() - time1) / 5))
    for ball in game_balls:
        ball.__update__()
        ball.__reflection__()
    for bullets in real_bullet:
        bullets.__update__(time1)
        bullets.__reflection__()
        if time.time() - bullets.start_time >= 5:  # пуля слишком долго-убираем
            real_bullet.remove(bullets)
        if (bullets.x - game_balls[0].x) ** 2 + (bullets.y - game_balls[0].y) ** 2 < (
                bullets.r + game_balls[0].r) ** 2:  # касание пули и мишени
            game_balls = [Balls()]
            print('VICTORY!!!')
    previous_click = click
    pygame.display.update()
    screen.fill((0, 0, 0))

pygame.quit()
