import pyglet
import pyglet.text as text
from pyglet.window import mouse
from pyglet.gl import *

import numpy as np

import utils
from bezier import Bezier

WIDTH = 1280
HEIGHT = 720

class Frame(pyglet.window.Window):
  elements = None
  pre_bezier = None

  label = None
  selected = None

  cx, cy = 0, 0
  m = None

  def __init__(self):
    super(Frame, self).__init__()
    self.set_size(WIDTH, HEIGHT)
    scr = pyglet.window.get_platform().get_default_display().get_default_screen()

    self.set_size(WIDTH, HEIGHT)
    self.set_location(int((scr.width-WIDTH)/2), int((scr.height-HEIGHT)/2))
    self.set_caption("EP1 - MAC0210 - Curvas de Bezier")

    self.elements = []
    self.pre_bezier = []
    self.label = text.Label("Pre-bezier points: 0",
                            font_name='Times New Roman', font_size=12,
                            x=10, y=25, anchor_y='center', color=(0, 0, 0, 255))

  def on_draw(self):
    self.clear()
    glClear(GL_COLOR_BUFFER_BIT)
    for e in self.elements:
      glPushAttrib(GL_CURRENT_BIT)
      e.draw()
      glPopAttrib(GL_CURRENT_BIT)
    n_pre_bezier = len(self.pre_bezier)
    if n_pre_bezier > 0:
      glPushAttrib(GL_CURRENT_BIT)
      glColor3f(0, 0, 1.0)
      for i in range(n_pre_bezier-1):
        utils.draw_circle(self.pre_bezier[i], 5, 10)
      glColor3f(0, 1.0, 0)
      utils.draw_circle(self.pre_bezier[-1], 5, 10)
      glPopAttrib(GL_CURRENT_BIT)
    glColor3f(0, 0, 0)
    self.label.draw()
    if self.m is not None:
      glPushAttrib(GL_CURRENT_BIT)
      glColor3f(0, 0, 0)
      glBegin(GL_LINES)
      glVertex2f(self.cx, self.cy)
      glVertex2f(self.m[0], self.m[1])
      glEnd()
      glPopAttrib(GL_CURRENT_BIT)

  def on_mouse_release(self, x, y, button, mods):
    if button == mouse.LEFT:
      if len(self.pre_bezier) >= 3:
        self.elements.append(Bezier(np.array(self.pre_bezier[0]), np.array(self.pre_bezier[1]),
                                    np.array(self.pre_bezier[2]), np.array((x, y))))
        self.pre_bezier = []
        self.label.text = "Pre-bezier points: 0"
      else:
        self.pre_bezier.append((x, y))
        self.label.text = "Pre-bezier points: " + str(len(self.pre_bezier))

  def on_mouse_motion(self, x, y, dx, dy):
    self.cx, self.cy = x, y
    if len(self.elements) > 0:
      min, imin = 0, 0
      for i, e in enumerate(self.elements):
        pm, d = e.distance(x, y)
        e.active = False
        if d > min:
          min, imin = d, i
          self.m = pm
      self.selected = self.elements[imin]
      self.selected.active = True

  def start(self):
    glClearColor(255, 255, 255, 1.0)
    glColor3i(0, 0, 0)
    pyglet.app.run()

