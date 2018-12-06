from pyglet.gl import *

import numpy as np

import utils

class Dataset:
  T = None
  Y = None
  n = None
  m = None
  max = None

  def __init__(self, fname=""):
    if fname == "":
      self.T = np.zeros(0)
      self.Y = np.zeros(0)
      self.n = 0
      self.m = 0
      return
    D = np.loadtxt(fname)
    self.T = D[:,0]
    self.Y = D[:,1]
    self.n = len(D)
    self.m = int(np.max(self.T)+1)
    self.max = np.max(self.Y)

  def add(self, t, y):
    self.T = np.insert(self.T, len(self.T), t)
    self.Y = np.insert(self.Y, len(self.Y), y)

  def draw(self, sx=1, sy=1):
    glColor3f(1.0, 0, 0)
    for i, _ in enumerate(self.T):
      utils.draw_circle((sx*self.T[i], sy*self.Y[i]), 2, 10)

  def get(self):
    return self.T, self.Y

class Dataset2D:
  x_data = None
  y_data = None

  def __init__(self, fname=""):
    self.x_data = Dataset()
    self.y_data = Dataset()
    if fname == "":
      return
    D = np.loadtxt(fname)
    self.x_data.T = D[:,0]
    self.x_data.Y = D[:,1]
    self.y_data.T = D[:,2]
    self.y_data.Y = D[:,3]

  def add(self, t0, y0, t1, y1):
    self.x_data.add(t0, y0)
    self.y_data.add(t1, y1)

  def get(self):
    T0, Y0 = self.x_data.get()
    T1, Y1 = self.y_data.get()
    return T0, Y0, T1, Y1
