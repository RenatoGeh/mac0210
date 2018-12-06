from pyglet.gl import *

import numpy as np
import numpy.linalg
import numpy.matlib

import matplotlib.pyplot as plt

def _simpson(n, k, i):
  s = _ddbeta(-i)*_ddbeta(-k)
  c = [4, 2]
  for t in range(n-1):
    s += _ddbeta(t-i)*_ddbeta(t-k)*c[t % 2]
  s += _ddbeta(n-i)*_ddbeta(n-k)
  return s/3

def _ddbeta(t):
  if abs(t) >= 2:
    return 0
  if t > 1:
    return -0.375*t + 0.75
  if t > 0:
    return 4.5*t - 3
  if t > -1:
    return -4.5*t - 3
  # t > -2
  return 0.375*t + 0.75

def _dbeta(t):
  if abs(t) >= 2:
    return 0
  s = t*t
  if t > 1:
    return 0.75*t - (0.1875*s + 0.75)
  if t > 0:
    return 2.25*s - 3*t
  if t > -1:
    return -(2.25*s + 3*t)
  # t > -2
  return 0.1875*s + 0.7*t + 0.75

def _beta(t):
  if t < 0:
    return _beta(-t)
  if t < 1:
    return (0.75*t - 1.5)*t*t + 1
  if t < 2:
    t = 2-t
    return t*t*t*0.25
  return 0

def _view_matrix(M):
  plt.matshow(M)
  plt.show()

def _compute_M(n):
  M = np.matlib.zeros((n, n))
  for i in range(n):
    for d in range(-4, 5):
      j = i+d
      if j >= 0 and j < n:
        M[i,j] = 2*_simpson(n, i, j)
  return M

class Spline:
  a = None
  n = None
  m = None
  M = None

  def __init__(self, n, m):
    self.n = n
    self.m = m
    self.M = _compute_M(m)

  # Fits this Spline with dataset D and L2 lambda l.
  def fit(self, D, l):
    T, Y = D.get()
    B = np.matlib.zeros((self.n, self.m))
    for i in range(self.n):
      for j in range(self.m):
        B[i,j] = _beta(T[i]-j)
    print("B", B.shape)
    print("M", self.M.shape)
    A = np.matmul(B.T, B) + l*self.M
    print("A", A.shape)
    print("Y", Y.shape)
    b = np.dot(B.T, Y)
    print("b", b.shape)
    self.a = np.linalg.solve(A, b.T)
    return self.a

  def s(self, t):
    z = 0
    for i in range(-4, 5):
      k = int(t)+i
      if k >= 0 and k < self.n:
        z += np.asscalar(self.a[k])*_beta(t-k)
    return z

  def draw(self, sx=1, sy=1):
    glBegin(GL_LINE_STRIP)
    glColor3f(0, 0, 1)
    i = 0
    while i < self.n:
      glVertex2i(int(sx*i), int(sy*self.s(i)))
      i += 0.15
    glEnd()

class Spline2D:
  x_spline = None
  y_spline = None

  def __init__(self, n, m):
    self.x_spline = Spline(n, m)
    self.y_spline = Spline(n, m)

  # Fits this Spline2D with Dataset2D D and L2 lambda l.
  def fit(self, D, l):
    self.x_spline.fit(D.x_data, l)
    self.y_spline.fit(D.y_data, l)

  def s(self, t):
    return self.x_spline(t), self.y_spline(t)

  def draw(self):
    self.x_spline.draw()
    self.y_spline.draw()
