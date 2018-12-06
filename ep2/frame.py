import math

import pyglet
import pyglet.text as text
import pyglet.app
from pyglet.window import mouse
from pyglet.window import key
from pyglet.gl import *

import numpy as np

from spline import Spline
import utils

WIDTH = 1280
HEIGHT = 720

class Frame(pyglet.window.Window):
  spline = None
  data = None
  n = None
  m = None

  def __init__(self, D, n, l):
    super(Frame, self).__init__()
    self.set_size(WIDTH, HEIGHT)
    scr = pyglet.window.get_platform().get_default_display().get_default_screen()

    self.set_size(WIDTH, HEIGHT)
    self.set_location(int((scr.width-WIDTH)/2), int((scr.height-HEIGHT)/2))
    self.set_caption("EP2 - MAC0210 - B-Splines")

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)

    self.data = D
    self.m = D.n
    self.n = n
    self.spline = Spline(self.n, self.m)
    self.spline.fit(D, l)

  def on_draw(self):
    self.clear()
    glClear(GL_COLOR_BUFFER_BIT)
    print("Drawing spline")
    sx, sy = WIDTH/self.m, 0.6*HEIGHT/self.data.max
    self.spline.draw(sx, sy)
    print("Drawing dataset points")
    self.data.draw(sx, sy)

  def on_key_press(self, sym, mods):
    if sym == key.ESCAPE:
      pyglet.app.exit()

  def start(self):
    glClearColor(255, 255, 255, 1.0)
    glColor3i(0, 0, 0)
    pyglet.app.run()

