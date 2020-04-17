
import math
import numpy as np
from OpenGL.GL import *

_tstack = [[[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]],
           [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]],
           [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]],
           [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]],
           [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]],
           [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]],
           [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]]

_normals = np.asfarray([(0,0,-1),
                                    (-1,0,0),
                                    (0,0,1),
                                    (1,0,0),
                                    (0,1,0),
                                    (0,-1,0)])

_verts = np.asfarray(((1,-1,-1),
                     (1,1,-1),
                     (-1,1,-1),
                     (-1,-1,-1),
                     (1,-1,1),
                     (1,1,1),
                     (-1,-1,1),
                     (-1,1,1)))

_surfaces =np.array(((3,0,1,2),
                                 (6,7,2,3),
                                 (6,7,5,4),
                                 (4,5,1,0),
                                 (1,5,7,2),
                                 (0,3,6,4)))


def TestForHit(position):
	global _tstack

	g = [0, 0, 0]
	g[0] = int(math.floor(position[0] + 3)) // 2
	g[1] = int(math.floor(position[1] + 3)) // 2
	g[2] = int(math.floor(position[2] + 3)) // 2
	if g[0] < 0 or g[0] > 3 or g[1] > 5 or g[2] < 0 or g[2] > 3:
		return False
	if not _tstack[g[1]][g[2]][g[0]] is None:
		return True
	g[1] = (math.ceil(position[1] + 5)) // 2
	if not _tstack[g[1]][g[2]][g[0]] is None:
		return True
	return False


def Add(position, color):
	global _tstack

	g = [0,0,0]
	g[0] = int(round(position[0] + 3)) // 2
	g[1] = int(round(position[1] + 3)) // 2
	g[2] = int(round(position[2] + 3)) // 2
	if g[0] < 0  or g[0] > 3 or g[1] > 5 or g[2] < 0 or g[2] > 3:
		return
	_tstack[g[1]][g[2]][g[0]] = np.asfarray(color.copy())

def CheckFill():
	global _tstack

	q = 0
	for y in range(6):
		missing = False
		for x in range(4):
			for z in range(4):
				if _tstack[y + q][z][x] is None:
					missing = True
					break
			if missing:
				break
		if not missing:
			_tstack.pop(y + q)
			_tstack.append([[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]])
			q -= 1

def Render(screen):
	global _tstack
	global _verts
	global _normals
	global _surfaces

	m = glGetDouble(GL_MODELVIEW_MATRIX)  # save matrix

	view = glGetDouble(GL_MODELVIEW_MATRIX)
	invT = np.linalg.inv(view).transpose()

	lightNormal = np.asfarray((0.0,0.0,1.0))

	for y in range(6):
		for x in range(4):
			for z in range(4):
				if _tstack[y][z][x] is None:
					continue
				os = glGetDouble(GL_MODELVIEW_MATRIX)

				glBegin(GL_QUADS)
				for n, surface in enumerate(_surfaces):
					for vertex in surface:
						vert = np.asfarray([_verts[vertex][0] + (x * 2) - 3,
						                   _verts[vertex][1] + (y * 2) - 5,
						                   _verts[vertex][2] + (z * 2) - 3])

						norm = np.append(_normals[n], 1)
						modelNorm = np.matmul(norm, invT)
						modelNorm = np.delete(modelNorm, 3)

						lenSqr2 = np.sum(modelNorm * modelNorm)
						len2 = math.sqrt(lenSqr2)
						modelNorm /= len2

						dot = np.sum(lightNormal * modelNorm)
						mult = max(min(dot,1),0)

						if mult > 0:
							glColor3fv(_tstack[y][z][x] * mult)
							glNormal3fv(_normals[n])
							glVertex3fv(vert)
				glEnd()

				glLoadMatrixf(os)
	glLoadMatrixf(m)