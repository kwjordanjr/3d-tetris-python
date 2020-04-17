
import pygame
from OpenGL.GL import *
import numpy as np
import math
import random
import ColorCube2
import copy
from scipy.spatial.transform import Rotation as R
import TStack


L = [[1,0.5,0],[(0,0,0),(2,0,0),(2,2,0),(-2,0,0)]]
I = [[0,0,1],[(-2,0,0),(0,0,0),(2,0,0),(4,0,0)]]
T = [[.5,0,1],[(-2,0,0),(0,0,0),(2,0,0),(0,2,0)]]
S = [[0,1,0], [(-2,0,0),(0,0,0),(0,2,0),(2,2,0)]]
O = [[1,1,0], [(0,0,0),(2,0,0),(2,2,0),(0,2,0)]]

blocks = [L,I,T,S,O]
_current = None

def RandBlock():
	global blocks
	global _current
	block = random.choice(blocks)
	_current = ColorCube2.ColorCube2(color=block[0], offsets=block[1])

_pos = [-1, 5, -1]
rot = R.from_quat([0,0,1,0])
_axis = 'y'
_lock = True
RandBlock()

def Rot(axis):
	global rot
	global _current
	global _lock

	fix = False

	#glRotate(90, *_curAng)
	rot = R.from_euler(axis, 90, degrees=True)
	if not _lock:
		for i in range(len(_current.offsets)):
			_current.offsets[i] = np.rint(rot.apply(list(_current.offsets[i])))
		_lock = True

def CheckSides():
	global _current
	fixL = False
	fixR = False
	fixU = False
	fixD = False

	for i in range(len(_current.offsets)):
		if _current.offsets[i][0] + _pos[0] < -4:
			fixL = True
			break
		elif _current.offsets[i][0] + _pos[0] > 4:
			fixR = True
			break
		elif _current.offsets[i][2] + _pos[2] < -4:
			fixU = True
			break
		elif _current.offsets[i][2] + _pos[2] > 4:
			fixD = True
			break
	if fixL:
		for i in range(len(_current.offsets)):
			_current.offsets[i][0] += 2
	elif fixR:
		for i in range(len(_current.offsets)):
			_current.offsets[i][0] -= 2
	elif fixU:
		for i in range(len(_current.offsets)):
			_current.offsets[i][2] += 2
	elif fixD:
		for i in range(len(_current.offsets)):
			_current.offsets[i][2] -= 2


def ProcessEvent(event):
	global _pos
	global _axis
	global _lock
	global _current
	no = False


	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_LEFT:
			for offset in _current.offsets:
				if offset[0] + _pos[0] < -1:
					no = True
			if not no:
				_pos[0] -= 2
		elif event.key == pygame.K_RIGHT:
			for offset in _current.offsets:
				if offset[0] + _pos[0] > 1:
					no = True
			if not no:
				_pos[0] += 2

		elif event.key == pygame.K_UP:
			for offset in _current.offsets:
				if offset[2] + _pos[2] < -1:
					no = True
			if not no:
				_pos[2] -= 2
		elif event.key == pygame.K_DOWN:
			for offset in _current.offsets:
				if offset[2] + _pos[2] > 1:
					no = True
			if not no:
				_pos[2] += 2

		elif event.key == pygame.K_a:
			_lock = False
			_axis = 'x'
		elif event.key == pygame.K_s:
			_lock = False
			_axis = 'y'
		elif event.key == pygame.K_d:
			_lock = False
			_axis = 'z'



def Update(deltaTime):
	global _current
	global _pos

	_pos[1] -= 3 * deltaTime

	bottom = False
	if _pos[1] <= -5:
		bottom = True


	if bottom:
		_pos[1] = math.ceil(_pos[1])

		RandBlock()
		_pos = [-1, 5, -1]

	_current.Update(deltaTime)


def Render(screen):
	global _current
	global _pos
	global rot
	global _curAng
	global _axis

	m = glGetDouble(GL_MODELVIEW_MATRIX)

	glTranslatef(*_pos)
	Rot(_axis)
	CheckSides()

	_current.Render(screen)

	glLoadMatrixf(m)


