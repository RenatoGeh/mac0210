from numpy.polynomial import polynomial as poly
from pyglet.window import mouse
import numpy as np
from pyglet.gl import *

class Box:
  active = None
  bounds = None

  def __init__(self):
    self.active = False
    self.bounds = [[0, 0], [0, 0]]

  # Rough intersection using bounding boxes.
  def rough_int(self, elements):
    pass

  def intersects(self, elements):
    pass

  def mouse_pressed(self, x, y, button, mods):
    if button == mouse.LEFT:
      self.bounds[0][0], self.bounds[0][1] = x, y

  def mouse_dragged(self, x, y, dx, dy, buttons, mods):
    if buttons & mouse.LEFT:
      self.active = True
      self.bounds[1][0], self.bounds[1][1] = x, y

  def mouse_released(self, x, y, button, mods):
    if button == mouse.LEFT:
      self.active = False
      self.bounds[1][0], self.bounds[1][1] = self.bounds[0][0], self.bounds[0][1]

  def draw(self):
    if self.active:
      glPushAttrib(GL_CURRENT_BIT)
      glColor4f(0.8, 0.8, 0.8, 0.5)
      glBegin(GL_POLYGON)
      glVertex2f(*self.bounds[0])
      glVertex2f(self.bounds[1][0], self.bounds[0][1])
      glVertex2f(*self.bounds[1])
      glVertex2f(self.bounds[0][0], self.bounds[1][1])
      glVertex2f(*self.bounds[0])
      glEnd()
      glPopAttrib(GL_CURRENT_BIT)

