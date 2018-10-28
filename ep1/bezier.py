from numpy.polynomial import polynomial as poly
from pyglet.gl import *

import utils

class Bezier:
  pts = None # Bezier point coordinates
  k = None # Bezier polynomial coefficients
  dk = None # Bezier polynomial derivative coefficients

  # Arguments p0, p1, p2 and p3 are (x, y) coordinates (a, b, c, d) of a Bezier curve described by
  # the polynomial:
  #  B(t) = a*(t-1)^3 + b*t*(t-1)^2 + c*(t-1)*t^2 + d*t^3
  def __init__(self, p0, p1, p2, p3):
    self.pts = [p0, p1, p2, p3]
    self.k = [[0.0 for _ in range(4)] for _ in range(2)]
    self.dk = [[0.0 for _ in range(3)] for _ in range(2)]
    self.recompute()

  def recompute(self):
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

  def draw(self):
    glColor3f(0.66, 0.66, 0.66)
    glBegin(GL_LINES)
    glVertex2f(self.pts[0][0], self.pts[0][1])
    glVertex2f(self.pts[1][0], self.pts[1][1])
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(self.pts[2][0], self.pts[2][1])
    glVertex2f(self.pts[3][0], self.pts[3][1])
    glEnd()
    glColor3f(0.0, 0.0, 0.0)
    self.__de_casteljau(self.pts)
    glColor3f(1.0, 0, 0)
    for p in self.pts:
      utils.draw_circle(p, 5, 10)

  # De Casteljau's algorithm
  def __de_casteljau(self, P):
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
    self.__de_casteljau((P[0], M[0], M[1], M[3]))
    self.__de_casteljau((M[3], M[5], M[4], P[3]))

  def f(self, t, axis=None):
    if axis is None:
      return (self.f(t, axis=0), self.f(t, axis=1))
    # Equivalent to B(t) = a*(t-1)^3 + b*t*(t-1)^2 + c*(t-1)*t^2 + d*t^3
    return poly.polyval(t, self.k[axis])

  def df(self, t, axis=None):
    if axis is None:
      return (self.df(t, axis=0), self.f(t, axis=1))
    # Equivalent to B'(t) = 3(3(b-c)-a+d)t^2 + 6(a-2b+c)t + 3(b-a)
    return poly.polyval(t, self.dk[axis])
