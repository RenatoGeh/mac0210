import math

from numpy.polynomial import polynomial as poly
from pyglet.window import mouse
import numpy as np
from pyglet.gl import *

import utils

# De Casteljau's algorithm for degree = 3.
def _de_casteljau(P):
  if utils.dist_seg(P[0], P[3], P[1]) <= 1 and utils.dist_seg(P[0], P[3], P[2]) <= 1:
    glBegin(GL_LINES)
    glVertex2f(P[0][0], P[0][1])
    glVertex2f(P[3][0], P[3][1])
    glEnd()
    return
  M = [None for _ in range(6)]
  M[0] = (P[0]+P[1])/2.0
  M[2] = (P[1]+P[2])/2.0
  M[4] = (P[2]+P[3])/2.0
  M[1] = (M[0]+M[2])/2.0
  M[5] = (M[2]+M[4])/2.0
  M[3] = (M[1]+M[5])/2.0
  _de_casteljau((P[0], M[0], M[1], M[3]))
  _de_casteljau((M[3], M[5], M[4], P[3]))

# De Casteljau's algorithm for degree = 2.
def _de_casteljau2(P):
  if utils.dist_seg(P[0], P[2], P[1]) <= 1:
    glBegin(GL_LINES)
    glVertex2f(P[0][0], P[0][1])
    glVertex2f(P[2][0], P[2][1])
    glEnd()
    return
  M = [None for _ in range(3)]
  M[0] = (P[0]+P[1])/2.0
  M[1] = (P[1]+P[2])/2.0
  M[2] = (M[0]+M[1])/2.0
  _de_casteljau2((P[0], M[0], M[2]))
  _de_casteljau2((M[2], M[1], P[2]))

class Bezier:
  pts = None # Bezier point coordinates
  k = None # Bezier polynomial coefficients
  dk = None # Bezier polynomial derivative coefficients
  degree = None # Bezier polynomial degree

  active = None # Sets this Bezier as the selected curve
  hide = None # Hides all decorations
  sel_vtx = None # Selected vertex

  # Arguments p0, p1, p2 and p3 are (x, y) coordinates (a, b, c, d) of a Bezier curve described by
  # the polynomial:
  #  B(t) = a*(t-1)^3 + b*t*(t-1)^2 + c*(t-1)*t^2 + d*t^3
  def __init__(self, p0, p1, p2, p3=None, degree=3):
    if degree != 2:
      degree = 3
      self.pts = [p0, p1, p2, p3]
    else:
      self.pts = [p0, p1, p2]
    self.k = [np.zeros(degree+1) for _ in range(2)]
    self.dk = [np.zeros(degree) for _ in range(2)]
    self.degree = degree
    self.active = False
    self.hide = False
    self.recompute()

  def recompute(self):
    if self.degree == 2:
      for i in range(2):
        a, b, c = self.pts[0][i], self.pts[1][i], self.pts[2][i]
        c1 = a-2*b+c
        c2 = 2*(b-a)
        c3 = a
        self.k[i][0] = c1
        self.k[i][1] = c2
        self.k[i][2] = c3
        self.dk[i][0] = c1 << 1
        self.dk[i][1] = c2
    else:
      for i in range(2):
        a, d = self.pts[0][i], self.pts[3][i]
        b, c = self.pts[1][i], self.pts[2][i]
        c1 = 3*(b-c)-a+d
        c2 = 3*(a-2*b+c)
        c3 = 3*(b-a)
        c4 = a
        self.k[i][0] = c1
        self.k[i][1] = c2
        self.k[i][2] = c3
        self.k[i][3] = c4
        self.dk[i][0] = 3*c1
        self.dk[i][1] = c2 << 1
        self.dk[i][2] = c3

  def cycle_vertex(self):
    if self.sel_vtx is None:
      self.sel_vtx = 0
    else:
      self.sel_vtx = (self.sel_vtx + 1)%(self.degree+1)

  def in_range(self, x, y):
    p = np.array([x, y])
    for i, q in enumerate(self.pts):
      if np.sum((q-p)**2) < 25:
        return i
    return None

  def mouse_pressed(self, x, y, button, mods):
    if button == mouse.LEFT:
      self.sel_vtx = self.in_range(x, y)

  def mouse_dragged(self, x, y, dx, dy, buttons, mods):
    if self.sel_vtx is not None:
      if buttons & mouse.LEFT:
        self.pts[self.sel_vtx][0] = x
        self.pts[self.sel_vtx][1] = y

  def draw(self):
    if not self.hide:
      glColor3f(0.66, 0.66, 0.66)
      if self.degree != 2:
        glBegin(GL_LINES)
        glVertex2f(self.pts[0][0], self.pts[0][1])
        glVertex2f(self.pts[1][0], self.pts[1][1])
        glEnd()
        glBegin(GL_LINES)
        glVertex2f(self.pts[2][0], self.pts[2][1])
        glVertex2f(self.pts[3][0], self.pts[3][1])
        glEnd()
      else:
        glBegin(GL_LINES)
        glVertex2f(self.pts[0][0], self.pts[0][1])
        glVertex2f(self.pts[1][0], self.pts[1][1])
        glVertex2f(self.pts[1][0], self.pts[1][1])
        glVertex2f(self.pts[2][0], self.pts[2][1])
        glEnd()
    c = (1.0, 0.0, 0.0)
    if self.active:
      c = (0.0, 1.0, 0.0)
    if self.hide:
      c = (0.0, 0.0, 0.0)
    glColor3f(*c)
    if self.degree == 2:
      _de_casteljau2(self.pts)
    else:
      _de_casteljau(self.pts)
    c = (1.0, 0, 0)
    if self.active:
      c = (0.85, 0.15, 0.73)
    glColor3f(*c)
    if not self.hide:
      for i, p in enumerate(self.pts):
        if self.active and i == self.sel_vtx:
          glColor3f(0, 1.0, 0)
          utils.draw_circle(p, 5, 10)
          glColor3f(*c)
        else:
          utils.draw_circle(p, 5, 10)

  def distance(self, x, y):
    fd = 2*np.polyadd(np.polymul(self.dk[0], np.polysub(self.k[0], np.array([0, 0, 0, x]))),
                      np.polymul(self.dk[1], np.polysub(self.k[1], np.array([0, 0, 0, y]))))
    rt = np.roots(fd)
    im, m = 0, math.inf
    for r in rt:
      if r.imag == 0 and r <= 1 and r >= 0:
        v = np.polyval(fd, r)
        if v < m:
          im, m = r, v
    p = self.f(im)
    q = np.array([x, y])
    p = utils.min_pts(p, self.pts[0], q)
    p = utils.min_pts(p, self.pts[self.degree], q)
    return p, np.sum((p-q)**2)

  def bounds(self):
    xmin, ymin, xmax, ymax = math.inf, math.inf, 0, 0
    for p in self.pts:
      if p[0] < xmin:
        xmin = p[0]
      if p[1] < ymin:
        ymin = p[0]
      if p[0] > xmax:
        xmax = p[0]
      if p[1] > ymax:
        ymax = p[1]
    return xmin, ymax, xmax, ymin

  def f(self, t, axis=None):
    if axis is None:
      return (self.f(t, axis=0), self.f(t, axis=1))
    # Equivalent to B(t) = a*(t-1)^3 + 3*b*t*(t-1)^2 + 3*c*(t-1)*t^2 + d*t^3, if degree = 3
    # Or            B(t) = a*(t-1)^2 + 2*b*t*(t-1) + c*t^2,                   if degree = 2
    return np.polyval(self.k[axis], t)

  def df(self, t, axis=None):
    if axis is None:
      return (self.df(t, axis=0), self.f(t, axis=1))
    # Equivalent to B'(t) = 3(3(b-c)-a+d)t^2 + 6(a-2b+c)t + 3(b-a), if degree = 3
    # Or            B'(t) = 2(a-2b+c)t + 2(b-a)                     if degree = 2
    return np.polyval(self.dk[axis], t)

