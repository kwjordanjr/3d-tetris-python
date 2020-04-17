
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class TetrisS:
    def __init__(self):
        self.id = "S"
        self.colors = ((0,1,0),
                       (0,.5,0),
                       (0,1,0),
                       (0,.5,0))

        self.verts = np.asfarray(((1,-3,-2),
         (1,1,-2),
         (1,1,0),
         (1,3,0),
         (1, 3, 2),
         (1, -1, 2),
         (1, -1, 0),
         (1, -3, 0),
         (-1, -3, -2),
         (-1, 1, -2),
         (-1, 1, 0),
         (-1, 3, 0),
         (-1, 3, 2),
         (-1, -1, 2),
         (-1, -1, 0),
         (-1, -3, 0)))

        self.surfaces = ((0,1,2,7),
           (6,3,4,5),
           (5,4,12,13),
           (13,12,11,14),
           (15,10,9,8),
           (6,5,13,14),
           (7,6,14,15),
           (0,7,15,8),
           (1,0,8,9),
           (2,1,9,10),
           (3,2,10,11),
           (4,3,11,12))

        self.ang = 0

        self.xAxis = 1
        self.yAxis = 0
        self.zAxis = 0

        self.time = 0
        self.dispY = 5
        self.dispX = 0
        self.dispZ = 0
        self.reset = False

    def ProcessEvent(self, event):
        if event.type == pygame.KEYUP and event.key == pygame.K_a:
            self.ang += 90
            self.xAxis, self.yAxis, self.zAxis = 1, 0, 0
            return True
        elif event.type == pygame.KEYUP and event.key == pygame.K_s:
            self.ang += 90
            self.xAxis, self.yAxis, self.zAxis = 0, 1, 0
            return True
        elif event.type == pygame.KEYUP and event.key == pygame.K_d:
            self.ang += 90
            self.xAxis, self.yAxis, self.zAxis = 0, 0, 1
            return True

        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            glTranslatef(0, 0, 2)
            self.dispZ += 2
            return True
        elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
            glTranslatef(0, 0, -2)
            self.dispZ -= 2
            return True
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            glTranslatef(-2, 0, 0)
            self.dispX -= 2
            return True
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            glTranslatef(2, 0, 0)
            self.dispX += 2
            return True
        return False

    def Update(self, deltaTime):
        self.time += deltaTime
        speed = -7 * deltaTime
        self.dispY += speed
        glTranslatef(0,speed,0)
        if self.time > 3:
            self.reset = True

    def DrawBlock(self):
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            for i, vert in enumerate(surface):
                glColor3fv(self.colors[i])
                glVertex3fv(self.verts[vert])
        glEnd()

    def Render(self, screen):
        m = glGetDouble(GL_MODELVIEW_MATRIX)  # save matrix
        glTranslate(0, 5, 0)
        glRotate(90, 0, 1, 0)
        glRotate(self.ang, self.xAxis, self.yAxis, self.zAxis)

        self.DrawBlock()

        glLoadMatrixf(m)
