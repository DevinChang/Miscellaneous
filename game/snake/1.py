# -*- coding: utf-8 -*-


import pygame, sys
from pygame.locals import *

pygame.init()


FPS = 30

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 400), 0, 32)

pygame.display.set_caption('Title')

WHITE = (255, 255, 255)

img = pygame.image.load('E:\Code\Python\Miscellaneous\game\snake\snake.jpg')
imgx = 10
imgy = 10

direction = 'right'

while True:
    screen.fill(WHITE)
    
    if direction == 'right':
        imgx += 5
        if imgx == 380:
            direction = 'down'
    elif direction == 'down':
        imgy += 5
        if imgy == 300:
            direction = 'left'
    elif direction == 'left':
        imgx -= 5
        if imgx == 10:
            direction = 'up'
    elif direction == 'up':
        imgy -= 5
        if imgy == 10:
            direction = 'right'
    
    screen.blit(img, (imgx, imgy))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.init()
            sys.exit()

    pygame.display.update()
    
    fpsClock.tick(FPS)
