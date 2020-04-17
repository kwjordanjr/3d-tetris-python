
from OpenGL.GL import *
import numpy as np
import math

from OpenGL.arrays import vbo
# from OpenGLContext.arrays import *
from OpenGL.GL import shaders


class ColorCube2:
    def __init__(self, color=[0, 0, 1], offsets=[(0, 0, 0)]):

        self.color = color
        self.offsets = np.asfarray(offsets)

        self.verts = np.float32([(1, -1, -1, color[0], color[1], color[2], 0, 0, -1),
                                 (1, 1, -1, color[0], color[1], color[2], 0, 0, -1),
                                 (-1, 1, -1, color[0], color[1], color[2], 0, 0, -1),
                                 (-1, -1, -1, color[0], color[1], color[2], 0, 0, -1),

                                 (-1, -1, -1, color[0], color[1], color[2], -1, 0, 0),
                                 (-1, 1, -1, color[0], color[1], color[2], -1, 0, 0),
                                 (-1, 1, 1, color[0], color[1], color[2], -1, 0, 0),
                                 (-1, -1, 1, color[0], color[1], color[2], -1, 0, 0),

                                 (-1, -1, 1, color[0], color[1], color[2], 0, 0, 1),
                                 (-1, 1, 1, color[0], color[1], color[2], 0, 0, 1),
                                 (1, 1, 1, color[0], color[1], color[2], 0, 0, 1),
                                 (1, -1, 1, color[0], color[1], color[2], 0, 0, 1),

                                 (1, -1, 1, color[0], color[1], color[2], 1, 0, 0),
                                 (1, 1, 1, color[0], color[1], color[2], 1, 0, 0),
                                 (1, 1, -1, color[0], color[1], color[2], 1, 0, 0),
                                 (1, -1, -1, color[0], color[1], color[2], 1, 0, 0),

                                 (1, 1, -1, color[0], color[1], color[2], 0, 1, 0),
                                 (1, 1, 1, color[0], color[1], color[2], 0, 1, 0),
                                 (-1, 1, 1, color[0], color[1], color[2], 0, 1, 0),
                                 (-1, 1, -1, color[0], color[1], color[2], 0, 1, 0),

                                 (1, -1, 1, color[0], color[1], color[2], 0, -1, 0),
                                 (1, -1, -1, color[0], color[1], color[2], 0, -1, 0),
                                 (-1, -1, -1, color[0], color[1], color[2], 0, -1, 0),
                                 (-1, -1, 1, color[0], color[1], color[2], 0, -1, 0)
                                 ])

        self.VERTEX_SHADER = shaders.compileShader("""#version 120
        uniform mat4 invT;
        attribute vec3 position;
        attribute vec3 color;
        attribute vec3 vertex_normal;
        varying vec4 vertex_color;
        void main()
        {
            vec4 norm = invT * vec4(vertex_normal,1.0);
            gl_Position = gl_ModelViewProjectionMatrix * vec4(position,1.0);
            vertex_color = vec4(color * min(1, max(0, norm[2])), 1.0);
        }""", GL_VERTEX_SHADER)

        self.FRAGMENT_SHADER = shaders.compileShader("""#version 120
        varying vec4 vertex_color;
        void main()
        {
            gl_FragColor = vertex_color;
        }""", GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(self.VERTEX_SHADER, self.FRAGMENT_SHADER)
        self.vbo = vbo.VBO(self.verts)

        self.uniformInvT = glGetUniformLocation(self.shader, "invT")
        self.position = glGetAttribLocation(self.shader, "position")
        self.colorAtt = glGetAttribLocation(self.shader, "color")
        self.vertex_normal = glGetAttribLocation(self.shader, "vertex_normal")

        self.ang = 0
        self.x_axis = 3
        self.y_axis = 1
        self.z_axis = 1

    def Update(self, deltaTime):
        self.ang += 50.0 * deltaTime

    def DrawBlock(self):
        shaders.glUseProgram(self.shader)
        glUniformMatrix4fv(self.uniformInvT, 1, True, np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX)))
        try:
            self.vbo.bind()
            try:
                glEnableVertexAttribArray(self.position)
                glEnableVertexAttribArray(self.colorAtt)
                glEnableVertexAttribArray(self.vertex_normal)
                glVertexAttribPointer(self.position, 3, GL_FLOAT, False, 36, self.vbo)
                glVertexAttribPointer(self.colorAtt, 3, GL_FLOAT, False, 36, self.vbo + 12)
                glVertexAttribPointer(self.vertex_normal, 3, GL_FLOAT, False, 36, self.vbo + 24)
                glDrawArrays(GL_QUADS, 0, 24)
            finally:
                self.vbo.unbind()
                glDisableVertexAttribArray(self.position)
                glDisableVertexAttribArray(self.colorAtt)
                glDisableVertexAttribArray(self.vertex_normal)
        finally:
            shaders.glUseProgram(0)

    def Render(self, screen):
        m = glGetDouble(GL_MODELVIEW_MATRIX)  # save matrix
        # glRotatef(self.ang, self.x_axis, self.y_axis, self.z_axis)

        for o in self.offsets:
            os = glGetDouble(GL_MODELVIEW_MATRIX)
            glTranslate(*o)
            self.DrawBlock()
            glLoadMatrixf(os)

        glLoadMatrixf(m)  # restore matrix
