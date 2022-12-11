import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))


rect(screen, (255, 0, 150), (0, 0, 400, 400)) #фон
circle(screen, (255, 255, 50), (200, 200), 100) #лицо
circle(screen, (0, 0, 0), (200, 200), 100, 3) #обводка
circle(screen, (0, 0, 0), (170, 170), 20) #правый глаз
circle(screen, (255, 0, 0), (170, 170), 7) #правый зрачок
circle(screen, (0, 0, 0), (235, 175), 30) #левый глаз
circle(screen, (255, 0, 0), (230, 175), 10) #левый зрачок
polygon(screen, (0, 0, 0), [(100, 100), (100, 85), (190, 130), (190, 145)]) #правая бровь
polygon(screen, (0, 0, 0), [(320, 130), (320, 115), (200, 130), (200, 145)]) #левая бровь
polygon(screen, (0, 0, 0), [(150, 235), (150, 250), (250, 250), (250, 235)]) #рот



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
