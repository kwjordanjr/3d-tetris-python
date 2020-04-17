
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

import Border


pygame.init()
size = width, height = 640, 900
screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width/height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

import GamePlay

glTranslatef(1.0,0.0, -20)
glRotate(-15, 0, 1, 0)
glRotate(30, 1, 0, 0)



def Update(deltaTime):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        GamePlay.ProcessEvent(event)

    GamePlay.Update(deltaTime)

    return True

def Render(screen):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    GamePlay.Render(screen)
    Border.Render(screen)
    pygame.display.flip()

clock = pygame.time.Clock()
while Update(float(clock.tick(60)) / 1000.0):
    Render(screen)

