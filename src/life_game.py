#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Controls:
Quit: q, alt+F4
Pause: spacebar
'''

import pygame
import numpy as np
import time
import sys

WIDTH, HEIGHT = 800, 800
nX, nY = 80, 80
xSize = WIDTH/nX
ySize = HEIGHT/nY

pygame.init()

screen = pygame.display.set_mode([WIDTH,HEIGHT])

BG_COLOR = (10,10,10)
LIVE_COLOR = (255,255,255)
DEAD_COLOR = (128,128,128)

status = np.zeros((nX,nY))

#Clock from pygame to register frames (*better than use time.sleep(1))
clock = pygame.time.Clock()

#Pause starts as default value so user can draw anything.
pauseRun = True

#Main game
while True:

    #Change framrate so it's more comfortable to draw something on it
    if pauseRun == False:
        clock.tick(10)
    else:
        clock.tick(60)
    
    #Save copy from original layout.
    newStatus = np.copy(status)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_q:
                print("Player quitted from the game.")
                pygame.quit()
                sys.exit()
            if event.key==pygame.K_SPACE:
                print("Game paused/unpaused.")
                pauseRun = not pauseRun

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            x, y = int(np.floor(posX/xSize)), int(np.floor(posY/ySize))
            #newStatus[x,y] = np.abs(newStatus[x,y]-1)
            newStatus[x,y] = not mouseClick[2]

    screen.fill(BG_COLOR) # Clean background

    #iterate over all the cells.
    for x in range(0,nX):
        for y in range(0,nY):

            if not pauseRun:

                nNeigh = status[(x-1)%nX,(y-1)%nY] + status[(x)%nX,(y-1)%nY] + \
                        status[(x+1)%nX,(y-1)%nY] + status[(x-1)%nX,(y)%nY] + \
                        status[(x+1)%nX,(y)%nY] + status[(x-1)%nX,(y+1)%nY] + \
                        status[(x)%nX,(y+1)%nY] + status[(x+1)%nX,(y+1)%nY]

                #1. One dead with 3 alive cells around revives.
                if status[x,y] == 0 and nNeigh==3:
                    newStatus[x,y] = 1

                #2. One alive cell with more than 3 around or less than 2 dies.
                elif status[x,y] == 1 and (nNeigh < 2 or nNeigh > 3):
                    newStatus[x,y] = 0

            poly = [(x*xSize,y*ySize),
                    ((x+1)*xSize,y*ySize),
                    ((x+1)*xSize,(y+1)*ySize),
                    (x*xSize,(y+1)*ySize)]

            if newStatus[x,y] == 1:
                pygame.draw.polygon(screen,LIVE_COLOR,poly,0)
            else:
                pygame.draw.polygon(screen,DEAD_COLOR,poly,1)

    status = np.copy(newStatus)
    pygame.display.flip()

#end -