import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

_lightVector = np.array([0,0,1])

class ColorCube:
    def __init__(self, color = [0,0,1], offsets = [(0,0,0)]):
        self.offsets = np.asfarray(offsets)

        self.color = np.asfarray(color)

        self.normals = np.asfarray([(0,0,-1),
                                    (-1,0,0),
                                    (0,0,1),
                                    (1,0,0),
                                    (0,1,0),
                                    (0,-1,0)])

        self.verts = np.asfarray(((1,-1,-1),
                                  (1,1,-1),
                                  (-1,1,-1),
                                  (-1,-1,-1),
                                  (1,-1,1),
                                  (1,1,1),
                                  (-1,-1,1),
                                  (-1,1,1)))

        self.surfaces =np.array(((3,0,1,2),
                                 (6,7,2,3),
                                 (6,7,5,4),
                                 (4,5,1,0),
                                 (1,5,7,2),
                                 (0,3,6,4)))

        self.ang = 0
        self.xAxis = 1
        self.yAxis = 1
        self.zAxis = 1


    def Update(self, deltaTime):
        self.ang += 50 * deltaTime

    def DrawBlock(self, invT):
        global _lightVector

        glBegin(GL_QUADS)
        for n, surface in enumerate(self.surfaces):
            for vertex in surface:
                norm = np.append(self.normals[n], 1)
                modelNorm = np.matmul(norm,invT)
                modelNorm = np.delete(modelNorm, 3)
                len = math.sqrt(np.sum(modelNorm*modelNorm))

                modelNorm /= len

                dot = np.sum(_lightVector*modelNorm)
                mult = max(min(dot, 1), 0)

                glColor3fv(self.color * mult)
                glVertex3fv(self.verts[vertex])
        glEnd()


    def Render(self, screen):
        m = glGetDouble(GL_MODELVIEW_MATRIX) #save matrix
        glRotate(self.ang, self.xAxis, self.yAxis, self.zAxis)

        view = glGetDouble(GL_MODELVIEW_MATRIX)
        invT = np.linalg.inv(view).transpose()

        for o in self.offsets:
            os = glGetDouble(GL_MODELVIEW_MATRIX)
            glTranslate(*o)
            self.DrawBlock(invT)
            glLoadMatrixf(os)

        #self.DrawBlock(invT)
        glLoadMatrixf(m)
