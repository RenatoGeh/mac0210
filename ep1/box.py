from numpy.polynomial import polynomial as poly
from pyglet.window import mouse
import numpy as np
from pyglet.gl import *

import utils

class Box:
  active = None
  bounds = None

  def __init__(self):
    self.active = False
    self.bounds = [[0, 0], [0, 0]]

  # Rough intersection using bounding boxes.
  def rough_int(self, elements):
    a1, b1, a2, b2 = *self.bounds[0], *self.bounds[1]
    for e in elements:
      x1, y1, x2, y2 = e.bounds()
      if x1 >= a1 and x2 <= a2 and y1 <= b1 and y2 >= b2:
        return e
    return None

  def intersects(self, elements):
    re = self.rough_int(elements)
    if re is not None:
      return re
    for e in elements:
      if utils.contains_pt(self.bounds[0], self.bounds[1], e.pts[0]) or \
         utils.contains_pt(self.bounds[0], self.bounds[1], e.pts[3]):
        return e
      xrt = np.roots(e.dk[0])
      yrt = np.roots(e.dk[1])
      for i, rx in enumerate(xrt):
        ry = yrt[i]
        if rx >= 0 and rx <= 1:
          v = e.f(rx)
          if utils.contains_pt(self.bounds[0], self.bounds[1], v):
            return e
        if ry >= 0 and ry <= 1:
          v = e.f(ry)
          if utils.contains_pt(self.bounds[0], self.bounds[1], v):
            return e
    return None

  def mouse_pressed(self, x, y, button, mods):
    if button == mouse.LEFT:
      self.bounds[0][0], self.bounds[0][1] = x, y

  def mouse_dragged(self, x, y, dx, dy, buttons, mods):
    if buttons & mouse.LEFT:
      self.active = True
      self.bounds[1][0], self.bounds[1][1] = x, y

  def mouse_released(self, x, y, button, mods, elements):
    if button == mouse.LEFT:
      self.active = False
      self.bounds[1][0], self.bounds[1][1] = self.bounds[0][0], self.bounds[0][1]
      return self.intersects(elements)
    return None

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

